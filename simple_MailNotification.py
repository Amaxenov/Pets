import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import gmail_settings as gs

test_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
test_receiver = 'TEST@mail.ru'

def send_email_warning(receiver=test_receiver, server=test_server, sender=gs.user,
                    password=gs.key, subject=gs.subject, message=gs.text):
    mssg = MIMEMultipart()
    mssg['From'] = sender
    mssg['To'] = receiver
    mssg['Subject'] = subject
    mssg.attach(MIMEText(message))

    server.login(sender, password)
    server.sendmail(mssg['From'], mssg['To'], mssg.as_string())
    server.quit()

send_email_warning()
