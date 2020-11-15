import telegram.ext as tg
from config import Config
import sys
import os
from threading import Thread

TOKEN = Config.API_KEY
SUDO_USERS = Config.SUDO_USERS
#OWNER_USERNAME = Config.OWNER_USERNAME
DB_URI = Config.SQLALCHEMY_DATABASE_URI

p = tg.PicklePersistence(filename="data")
updater = tg.Updater(TOKEN, persistence=p, use_context=True)
dp = updater.dispatcher


def main():

    from afk import AFK_HANDLER, AFK2_HANDLER, AFK_GROUP, NO_AFK_GROUP, NO_AFK_HANDLER, AFK_REPLY_HANDLER, AFK_REPLY_GROUP
    from users import USER_HANDLER, USERS_GROUP, AF_HANDLER, BROADCAST_HANDLER, CHATLIST_HANDLER
    from start import START_HANDLER, HELP_HANDLER
    import lang

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

    dp.add_handler(tg.CommandHandler(
        "r", restart, filters=tg.Filters.user(SUDO_USERS)))
    dp.add_handler(START_HANDLER)
    # dp.add_handler(CHANGE_LANGUAGE_HANDLER)
    # dp.add_handler(SELECT_LANGUAGE_HANDLER)
    dp.add_handler(HELP_HANDLER)
    dp.add_handler(AFK_HANDLER, AFK_GROUP)
    dp.add_handler(AFK2_HANDLER, AFK_GROUP)
    dp.add_handler(NO_AFK_HANDLER, NO_AFK_GROUP)
    dp.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)
    dp.add_handler(USER_HANDLER, USERS_GROUP)
    dp.add_handler(AF_HANDLER)
    dp.add_handler(BROADCAST_HANDLER)
    dp.add_handler(CHATLIST_HANDLER)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
