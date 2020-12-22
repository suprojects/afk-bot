from telegram.ext import PicklePersistence, Updater
from secrets import BOT_TOKEN


p = PicklePersistence(
    filename="data"
)
updater = Updater(
    BOT_TOKEN,
    persistence=p,
    use_context=True
)
dp = updater.dispatcher


def main():
    import sys
    import os
    from threading import Thread
    from telegram.ext import CommandHandler, Filters
    from handlers import all_handlers
    from secrets import SUDO_USERS, SUDO

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

    for handler in all_handlers:
        if len(handler) == 2:
            if handler[0] == "error":
                dp.add_error_handler(
                    handler[1]
                )
            else:
                dp.add_handler(
                    handler[0],
                    handler[1]
                )
        else:
            dp.add_handler(
                handler[0]
            )

    dp.add_handler(
        CommandHandler(
            "r", restart, filters=SUDO
        )
    )

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == "__main__":
    main()
