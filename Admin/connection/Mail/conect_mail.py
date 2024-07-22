from dotenv import load_dotenv
import smtplib
import os


def connec_buzon():
    load_dotenv()
    mail=os.getenv('user_mail')
    password = os.getenv('password_mail')
    smtp = os.getenv('smtp')
    port = os.getenv('port')

    
    server = smtplib.SMTP(smtp, port)
    server.starttls()
    server.login(mail, password)
    
    return server, mail
    