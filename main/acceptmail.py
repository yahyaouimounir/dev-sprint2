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

def sendMail(user, id_user, event_name, email):
    # Email configuration
    sender_email = "amineaminea1234567890z@gmail.com"
    receiver_email = email
    password = "dqej nzld hkdy idpx"

    # Generate QR code in memory
    img_buffer = generate_qr_code_in_memory(id_user)

    # Create email message
    msg = MIMEMultipart()
    msg['Subject'] = f"🎉 Official Acceptance to {event_name} | Club Scientifique de l'ESI"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # HTML email body with retro theme
    html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://use.typekit.net/your-kit-id.css">
        <title>Event Acceptance</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Vaguely Retro', sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-image: url('https://drive.google.com/uc?export=view&id=15xm-SUWBMj6J7L82aDwXvsbMKyWwi7kf'); background-size: cover; background-position: center; margin: 0 auto; border-radius: 10px; overflow: hidden;">
            <tr>
                <td align="center" style="padding: 20px 0;">
                    <table border="0" cellpadding="0" cellspacing="0" width="600" style="color: white;">
                        <tr>
                            <td align="center" style="padding: 20px;">
                                <img src="https://drive.google.com/uc?export=view&id=1Ns9GpWD5FtGnCA7VM_b_FzFC1bGKkfYK" alt="Club Scientifique de l'ESI" style="width: 235px;">
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 30px;">
                                <h1 style="color: #EBD1B4; font-size: 24px;">Dear {user}</h1>
                                <p style="font-size: 16px; line-height: 1.6; color: #ffffff;">
                                    Big news! You've been officially accepted to participate in <strong>{event_name}</strong>! 🚀
                                </p>
                                <p style="font-size: 16px; line-height: 1.6; color: #ffffff;">
                                    Your unique event QR code is attached - this golden ticket grants you access to:
                                </p>
                                <ul style="color: #ffffff; font-size: 16px;">
                                    <li>Exclusive workshops</li>
                                    <li>Technical sessions</li>
                                    <li>Networking opportunities</li>
                                </ul>
                                
                                <div style="background-color: rgba(1, 161, 151, 0.2); padding: 20px; border-radius: 8px; margin: 25px 0;">
                                    <h3 style="color: #EBD1B4; margin: 0 0 15px 0;">Your Next Steps</h3>
                                    <p style="margin: 0; color: #ffffff;">
                                        1. Save this email with your QR code<br>
                                        2. Join our official Slack channel below<br>
                                        3. Prepare for an unforgettable experience!
                                    </p>
                                </div>

                                <p align="center" style="margin: 30px 0;">
                                    <a href="#" style="background-color: #01A197; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-size: 16px; display: inline-block;">
                                        Join Event Slack Channel
                                    </a>
                                </p>
                            </td>
                        </tr>
                        <tr>
                            <td align="center" style="padding: 20px 30px;">
                                <h2 style="font-size: 32px; color: #ffffff; margin: 20px 0;">{event_name} Awaits!</h2>
                                <p style="font-size: 16px; color: #ffffff;">
                                    Attached QR code required for:<br>
                                    <span style="color: #EBD1B4;">• Registration</span> | 
                                    <span style="color: #EBD1B4;">• Session Access</span> | 
                                    <span style="color: #EBD1B4;">• Special Activities</span>
                                </p>
                                
                                <div style="margin: 30px 0;">
                                    <img src="https://drive.google.com/uc?export=view&id=1Z0SLe3ZiN_-Fb-DY6ZXt1da-tbBhtE5g" alt="Event Branding" style="width: 200px;">
                                </div>
                                
                                <p style="font-size: 14px; color: #EBD1B4;">
                                    Need help? Contact our team:<br>
                                    <a href="mailto:events@cse-esi.dz" style="color: #01A197; text-decoration: none;">events@cse-esi.dz</a>
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>"""

    # Attach HTML version
    msg.attach(MIMEText(html, 'html'))

    # Attach QR code
    img_data = img_buffer.getvalue()
    img = MIMEImage(img_data, name=f"CSE_{event_name}_Pass.png")
    img.add_header('Content-Disposition', 'attachment', filename=f"Your_Exclusive_{event_name}_Pass.png")
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
