import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send phishing emails
def send_phishing_email(smtp_server, port, sender_email, sender_password, recipient_email):
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Urgent: Your Account Has Been Compromised!"

        # Phishing link with tracking
        tracking_link = f"http://localhost:5000/track_click?email={recipient_email}"

        # Email body
        body = f"""
        <html>
          <body>
            <h1>Action Required: Account Verification</h1>
            <p>We've noticed unusual activity in your account. Please click the link below to verify your account:</p>
            <a href="{tracking_link}">Verify Your Account</a>
          </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print(f"Phishing email sent to {recipient_email}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == '__main__':
    send_phishing_email(
        smtp_server='smtp.gmail.com',
        port=587,
        sender_email='your_email@gmail.com',
        sender_password='your_password',
        recipient_email='target_email@example.com'
    )
