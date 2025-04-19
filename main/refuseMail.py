import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendRefuseMail(user, event_name, email):    
    # Email configuration
    sender_email = "amineaminea1234567890z@gmail.com"
    receiver_email = email
    password = "dqej nzld hkdy idpx"  # Use app-specific password if 2FA is enabled

    # Create email message
    msg = MIMEMultipart()
    msg['Subject'] = f"Application Status Update for {event_name}"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Email body
    body = f"""Dear {user},

Thank you for your application to {event_name}.

After careful consideration, we regret to inform you that your application 
has not been accepted for this year's event. The selection process was 
particularly competitive with a large number of high-quality applications.

We genuinely appreciate your interest and encourage you to:
- Apply again for future events
- Follow our social channels for updates
- Participate in our community forums

Thank you again for your time and effort in applying.

Best regards,
The {event_name} Team"""
    
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Rejection email sent successfully!")
        return "send"
    except Exception as e:
        print(f"Error sending email: {e}")
        return "error"
    finally:
        server.quit()