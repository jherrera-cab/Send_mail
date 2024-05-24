from dotenv import load_dotenv
import os

load_dotenv()
user=os.getenv('user')

print (user)

