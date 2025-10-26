# Kandinsky 2.2 Text-to-Image Generation Web App

## Project Overview
This project is a Flask-based web application that allows users to generate high-quality images from text prompts using the **Kandinsky 2.2** model. The web application provides an intuitive UI with user authentication, OTP-based sign-up/login, and image history management. All generated images are stored locally and can be accessed later by users. The application ensures secure authentication and smooth user experience.

## Features

### 1. **User Authentication**
- Users must **sign up** before accessing the application.
- Sign-up requires **full name, phone number, and password**.
- OTP verification is mandatory for **sign-up** and **forgot password** functionalities.
- Secure **login** using phone number and password.
- Users cannot access any page without logging in.
- **Logout** feature to end user sessions.

### 2. **Text-to-Image Generation**
- Users enter a text prompt to generate an image.
- The **Kandinsky 2.2** model processes the prompt and creates an image.
- Generated images are saved in a local directory for future reference.
- Image generation balances speed and quality.

### 3. **User-Specific Image History**
- Each user's generated images are stored and displayed on a history page.
- Users can **delete individual images** or clear their entire history.

### 4. **Responsive Web UI**
- Neat and professional UI with a color scheme of **#31473A (dark green)** and **#EDF4F2 (light grayish-white)**.
- **Bootstrap and custom CSS** for an aesthetically pleasing layout.
- **JS scripts** enhance user interactions.

### 5. **Additional Pages**
- **About Us:** Provides details about the project.
- **Contact Us:** Allows users to submit inquiries.

## Tech Stack

### **Backend**
- **Python 3.11.0**
- **Flask 3.0.0** (Microframework for web development)
- **SQLite** (Lightweight database for storing user and image data)
- **bcrypt** (Secure password hashing)
- **Twilio** (OTP verification via SMS)

### **Machine Learning Model**
- **Kandinsky 2.2** (Diffusion-based text-to-image model)
- **PyTorch 2.2.1** (Framework for deep learning inference)
- **Diffusers 0.25.0** (Library for using diffusion models)

### **Frontend**
- **HTML, CSS, JavaScript** (Core web technologies)
- **Bootstrap** (UI framework for responsiveness)
- **Custom CSS** for enhanced design

## Installation & Setup

### 1. **Clone the Repository**
```bash
git clone https://github.com/Ash-Geek8/img_generation.git
cd img_generation
```

### 2. **Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Configure Twilio for OTP Authentication**
- Sign up for a **Twilio** account and get API credentials.
- Set up `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_PHONE_NUMBER`.

### 5. **Run the Application**
```bash
python app.py
```
- The app will be accessible at `http://127.0.0.1:5000/`

## Usage Guide

### 1. **Sign Up & Login**
- Navigate to the **Sign Up** page and enter details.
- Enter the OTP received via SMS to verify the phone number.
- Once signed up, log in using your phone number and password.

### 2. **Generate Images**
- After logging in, enter a text prompt in the **Generate** section.
- Click the "Generate" button to create an image.
- The generated image is saved in the local directory.

### 3. **View & Manage History**
- Access the "History" page to view all previously generated images.
- Delete individual images or clear the entire history.

### 4. **Other Features**
- Visit the "About Us" page to learn more about the project.
- Use the "Contact Us" page to send feedback or inquiries.

## Security Measures
- **Passwords are securely hashed** using bcrypt.
- **OTP verification** ensures valid phone numbers for authentication.
- **Session-based authentication** prevents unauthorized access.

## Deployment
To deploy this project on a cloud platform like **AWS, Render, or Railway**, follow these steps:

### 1. **Use Gunicorn for Production**
```bash
pip install gunicorn
```
Run the app with:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 2. **Deploy to AWS/Render**
- Set up an **EC2 instance** or **Render web service**.
- Configure **Twilio credentials** in environment variables.
- Run the Flask app using Gunicorn.

## Future Enhancements
- **Cloud Storage Integration**: Store images in **AWS S3** instead of local storage.
- **Model Optimization**: Improve **inference speed** for better user experience.
- **Multi-language Support**: Add UI translations for **global accessibility**.

## Contributors
- **Ashfaq Ahamed** - Lead Developer

## License
This project is open-source and licensed under the **MIT License**.

## Contact
For any queries, reach out via:
- **Email:** ashfaqahamed414@gmail.com
- **GitHub:** [Ash-Geek8](https://github.com/Ash-Geek8)
- **Phone:** +919092489855
- **GitHub Issues**: [Open an issue](https://github.com/Ash-Geek8/img_generation/issues)

---

This README provides a **detailed technical explanation** of the project and serves as a complete guide for developers and users. 🚀

