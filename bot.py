from telegram.ext import PicklePersistence, Updater
from config import Config


TOKEN = Config.API_KEY
SUDO_USERS = Config.SUDO_USERS

DB_URI = Config.SQLALCHEMY_DATABASE_URI

p = PicklePersistence(filename="data")
updater = Updater(TOKEN, persistence=p, use_context=True)
dp = updater.dispatcher


def main():
    # if invention isn't this, what invention has to be XD
    # ;P
    import sys
    import os
    import importlib
    from threading import Thread
    from telegram.ext import CommandHandler, Filters

    handlers = ('start', 'users', 'afk', 'lang')

    loaded = []

    for handler in handlers:
        loaded = loaded + importlib.import_module(handler).__handlers__

    handlers = loaded

    for handler in handlers:
        if len(handler) == 2:
            dp.add_handler(
                handler[0],
                handler[1]
            )
        else:
            dp.add_handler(
                handler[0]
            )

    if "-r" in sys.argv:
        for SUDO_USER in SUDO_USERS:
            updater.bot.send_message(SUDO_USER, "Bot restarted successfully.")

    def stop_and_restart():
        os.system("git pull")
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv, "-r")

    def restart(update, context):
        update.message.reply_text("Bot is restarting...")
        Thread(target=stop_and_restart).start()

    dp.add_handler(
        CommandHandler(
            "r", restart, filters=Filters.user(SUDO_USERS)
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
