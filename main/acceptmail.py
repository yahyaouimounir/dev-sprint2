import smtplib
import qrcode
from io import BytesIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def generate_qr_code_in_memory(data: str):
    """Generate QR code and return it as bytes in memory"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill="black", back_color="white")
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return img_buffer

def sendMail(user,id_user,event_name,email):
    
    # Email configuration
    sender_email = "amineaminea1234567890z@gmail.com"
    receiver_email = email
    password = "dqej nzld hkdy idpx"  # Use app-specific password if 2FA is enabled

    # Generate QR code in memory
    img_buffer = generate_qr_code_in_memory(id_user)

    # Create email message
    msg = MIMEMultipart()
    msg['Subject'] = f"Congratulations! You're Accepted to {event_name}"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Email body
    body = f"""Congratulations {user}!

We are thrilled to inform you that your application to {event_name} has been accepted!
Your QR code is attached to this email - please present it at the event entrance.

Looking forward to seeing you there!"""
    
    msg.attach(MIMEText(body, 'plain'))

    # Attach QR code from memory
    img_data = img_buffer.getvalue()
    img = MIMEImage(img_data, name=f"qrcode_{user}.png")
    img.add_header('Content-Disposition', 'attachment', filename=f"qrcode_{user}.png")
    msg.attach(img)

    # Send email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
        return "send"
    except Exception as e:
        print(f"Error sending email: {e}")
        return "error"
    finally:
        server.quit()
        img_buffer.close()

