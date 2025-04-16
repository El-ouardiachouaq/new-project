from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(override=True)

app = Flask(__name__)

# Print raw environment variables
print("Raw Environment Variables:")
print(f"EMAIL_USER: {os.environ.get('EMAIL_USER')}")
print(f"MAIL_DEFAULT_SENDER: {os.environ.get('MAIL_DEFAULT_SENDER')}")

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', os.environ.get('EMAIL_USER'))

# Initialize mail
mail = Mail(app)

# Print configuration
print("\nEmail Configuration:")
print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
print(f"MAIL_USE_TLS: {app.config['MAIL_USE_TLS']}")
print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
print(f"MAIL_DEFAULT_SENDER: {app.config['MAIL_DEFAULT_SENDER']}")

# Send test email
with app.app_context():
    try:
        msg = Message('Test Email',
                     sender=('Diffusion Calculator', app.config['MAIL_DEFAULT_SENDER']),
                     recipients=[app.config['MAIL_USERNAME']])
        msg.body = 'This is a test email to verify the email configuration.'
        mail.send(msg)
        print("\nTest email sent successfully!")
    except Exception as e:
        print(f"\nError sending email: {e}") 