import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


host = os.getenv("HOST")
database_name = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
app_secret = os.getenv("SECRET_KEY")
db_param = {
    "host": host,  # define with  host, like "127.0.0.1"
    "database": database_name,  # database name
    "user": user,  # database  username
    "password": password  # database password
    }
