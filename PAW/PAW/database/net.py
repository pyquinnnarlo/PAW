import smtplib
from email.mime.text import MIMEText


class Net:
    def send_email(self, to_email, subject, message):
            # Configure your email server
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'PAW'
            smtp_password = 'Py.quinn$narlo1'

            # Create an email message
            email_message = MIMEText(message)
            email_message['Subject'] = subject
            email_message['From'] = smtp_username
            email_message['To'] = to_email

            # Connect to the SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, [to_email], email_message.as_string())
