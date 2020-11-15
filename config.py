import os

class Config():
    SUDO_USERS = [951435494, 1178472788]
    API_KEY = os.environ.get("TOKEN", "Your TOKEN here")
    SQLALCHEMY_DATABASE_URI = "sqlite:///main.db" # postgresql db uri
