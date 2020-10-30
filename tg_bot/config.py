from tg_bot.sample_config import Config


class Development(Config):
    OWNER_ID = 951435494  # my telegram ID
    OWNER_USERNAME = "su_Theta"  # my telegram username
    API_KEY = "1457211149:AAHk2ZPkBP-u2UNZHoCIeHq6Hc-43KzQaeo"  # my api key, as provided by the botfather
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass@localhost:5432/afkdb'  # sample db credentials
    MESSAGE_DUMP = '-1234567890' # some group chat that your bot is a member of
    SUDO_USERS = []  # List of id's for users which have sudo access to the bot.
    LOAD = []
