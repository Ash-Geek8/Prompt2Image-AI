document.getElementById('contactForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    alert("Message sent successfully!");
});

function generateImage() {
    let prompt = document.getElementById('prompt').value;
    fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        if (data.image_url) {
            let img = document.createElement('img');
            img.src = data.image_url;
            document.getElementById('image-display').appendChild(img);
        }
    });
}

function deleteImage(filename) {
    fetch(`/delete/${filename}`, { method: 'DELETE' })
    .then(() => location.reload());
}

function clearHistory() {
    fetch('/clear_history', { method: 'POST' })
    .then(() => location.reload());
}

document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.querySelector("form");
    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            const phone = document.querySelector("input[name='phone']").value;
            if (!/^\d{10}$/.test(phone)) {
                alert("Enter a valid 10-digit phone number.");
                event.preventDefault();
            }
        });
    }
});
