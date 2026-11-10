import smtplib
import subprocess
from email.message import EmailMessage

class EmailHandler:
    def mutt(self, file="threat_ip.log"):
        subprocess.run(["bash", "mutt.sh", file], capture_output=True, text=True)
    
    def smtp_mailer_main(self):
        try:
            sender = "client_sender@gmail.com"
            key = "mail_one_time_password_generated"  # Use an app password for Gmail
            receiver = "client_receiver@gmail.com"
            body = f"threat detected .... check your server"
            subject = "ALERT MAIL FROM SERVER"
            msg = EmailMessage()
            msg['subject'] = subject
            msg['from'] = sender
            msg['to'] = receiver
            msg.set_content(body)
            # send the alert email without attaching the full log file for speed
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(sender, key)
                server.send_message(msg)
        except Exception as error:
            print(f"Error sending email: {error}")