import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_activation_email(user_email):
    msg = MIMEMultipart()
    msg['From'] = 'art.gasparyan.420@gmail.com'
    msg['To'] = user_email
    msg['Subject'] = 'Account Activation'


    body = """
    Hello,

    Thank you for registering. Please click the link below to activate your account:

    http://127.0.0.1:8000/docs#/default/user/me # Replace with your activation URL
    """.format(user_email)

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your email provider's SMTP server and port
    server.starttls()
    server.login('art.gasparyan.420@gmail.com', 'cbgykptgbehvazat')  # Replace with your email and password

    server.sendmail('art.gasparyan@gmail.com', user_email, msg.as_string())
    server.quit()

