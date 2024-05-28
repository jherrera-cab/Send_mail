from dotenv import load_dotenv
import os


def connec_buzon():
    load_dotenv()
    mail=os.getenv('user')
    password = os.getenv('password')

    print(password)