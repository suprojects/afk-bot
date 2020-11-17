import os

if os.environ.get("TOKEN", "N") == "N" or os.environ.get("DATABASE_URL", "N") == "N":
    print("Please specify TOKEN and DATABASE_URL environment variables before starting the bot.")
    exit()

class Config():
    SUDO_USERS = [951435494, 1178472788]
    API_KEY = os.environ.get("TOKEN")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
