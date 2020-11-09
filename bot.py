import telegram.ext as tg
from config import Config
import sys
import os
from threading import Thread

TOKEN = Config.API_KEY
SUDO_USERS = Config.SUDO_USERS
#OWNER_USERNAME = Config.OWNER_USERNAME
DB_URI = Config.SQLALCHEMY_DATABASE_URI

updater = tg.Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def main():
	
	from afk import AFK_HANDLER, AFK_GROUP, NO_AFK_GROUP, NO_AFK_HANDLER, AFK_REPLY_HANDLER, AFK_REPLY_GROUP
	from users import USER_HANDLER, USERS_GROUP, BROADCAST_HANDLER, CHATLIST_HANDLER
	from start import START_HANDLER, HELP_HANDLER, BTN_HANDLER, SL_HANDLER
	
	if "-r" in sys.argv:
		for SUDO_USER in SUDO_USERS:
			updater.bot.send_message(SUDO_USER, "Bot restarted successfully.")

	def stop_and_restart():
		os.system("git pull")
		updater.stop()
		os.execl(sys.executable, sys.executable, *sys.argv, "-r")

	def restart(update, context):
		update.message.reply_text("Bot is restarting...")
		Thread(target = stop_and_restart).start()

	dispatcher.add_handler(tg.CommandHandler("r", restart, filters = Filters.user(SUDO_USERS)))
	dispatcher.add_handler(START_HANDLER)
	dispatcher.add_handler(HELP_HANDLER)
	dispatcher.add_handler(SL_HANDLER)
	dispatcher.add_handler(BTN_HANDLER)
	dispatcher.add_handler(AFK_HANDLER, AFK_GROUP)
	dispatcher.add_handler(NO_AFK_HANDLER, NO_AFK_GROUP)
	dispatcher.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)
	dispatcher.add_handler(USER_HANDLER, USERS_GROUP)
	dispatcher.add_handler(BROADCAST_HANDLER)
	dispatcher.add_handler(CHATLIST_HANDLER)
	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
	main()
