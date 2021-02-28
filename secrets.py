import os

if not os.environ.get("TOKEN") or not os.environ.get("DATABASE_URL"):
    print("Please specify TOKEN and DATABASE_URL environment variables before starting the bot.")
    exit()

from telegram.ext import Filters

BOT_TOKEN = os.environ.get("TOKEN")
DB_URI = os.environ.get("DATABASE_URL")
SUDO_USERS = [
    1412086585
]
SUDO = Filters.user(SUDO_USERS)
LOG_CHAT = -1001336747262
