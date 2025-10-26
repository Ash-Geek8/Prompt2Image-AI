from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from diffusers import KandinskyV22Pipeline
import torch
import os
import random
import string
import sqlite3
import bcrypt
from twilio.rest import Client

# Initialize Flask App
app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session management

# Twilio Configuration for OTP
TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Database Setup
DB_PATH = "users.db"
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          full_name TEXT,
                          phone TEXT UNIQUE,
                          password TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id INTEGER,
                          file_name TEXT,
                          FOREIGN KEY(user_id) REFERENCES users(id))''')
        conn.commit()
init_db()

# Ensure image storage directory exists
SAVE_DIR = "static/generated_images"
os.makedirs(SAVE_DIR, exist_ok=True)

# Load model once and cache it
print("Loading Kandinsky 2.2 Model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = KandinskyV22Pipeline.from_pretrained("kandinsky-community/kandinsky-2-2-decoder").to(device)
print("Model Loaded Successfully!")

def send_otp(phone):
    otp = ''.join(random.choices(string.digits, k=6))
    session['otp'] = otp
    message = client.messages.create(
        body=f"Your verification OTP is: {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )
    return otp

@app.route('/')
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    user_id = session["user"]["id"]
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT file_name FROM images WHERE user_id = ?", (user_id,))
        images = cursor.fetchall()
    return render_template("index.html", first_name=session["user"]["full_name"].split()[0], images=[img[0] for img in images])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        send_otp(phone)
        session['signup_data'] = {'full_name': full_name, 'phone': phone, 'password': hashed_password}
        return redirect(url_for('verify_otp'))
    return render_template('signup.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session.get('otp'):
            data = session.pop('signup_data', None)
            if data:
                with sqlite3.connect(DB_PATH) as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO users (full_name, phone, password) VALUES (?, ?, ?)", (data['full_name'], data['phone'], data['password']))
                    conn.commit()
            return redirect(url_for('login'))
        return "Invalid OTP. Try again."
    return render_template('verify_otp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name, password FROM users WHERE phone = ?", (phone,))
            user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode(), user[2].encode()):
            session['user'] = {'id': user[0], 'full_name': user[1]}
            return redirect(url_for('home'))
        return "Invalid credentials."
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        phone = request.form['phone']
        send_otp(phone)
        session['reset_phone'] = phone
        return redirect(url_for('reset_password'))
    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        new_password = request.form['new_password']
        if entered_otp == session.get('otp'):
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password = ? WHERE phone = ?", (hashed_password, session.pop('reset_phone')))
                conn.commit()
            return redirect(url_for('login'))
        return "Invalid OTP. Try again."
    return render_template('reset_password.html')

@app.route('/history')
def history():
    if "user" not in session:
        return redirect(url_for("login"))
    user_id = session["user"]["id"]
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT file_name FROM images WHERE user_id = ?", (user_id,))
        images = cursor.fetchall()
    return render_template("history.html", images=[img[0] for img in images])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/generate', methods=['POST'])
def generate():
    if "user" not in session:
        return redirect(url_for("login"))
    text_prompt = request.form.get("prompt")
    if not text_prompt:
        return "No prompt provided", 400
    user_id = session["user"]["id"]
    image_name = f"{user_id}_{random.randint(1000, 9999)}.png"
    image_path = os.path.join(SAVE_DIR, image_name)
    image = model(text_prompt).images[0]
    image.save(image_path)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO images (user_id, file_name) VALUES (?, ?)", (user_id, image_name))
        conn.commit()
    return redirect(url_for("history"))

if __name__ == '__main__':
    app.run(debug=True)
