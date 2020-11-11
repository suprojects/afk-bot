from bot import dispatcher
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler

bot = dispatcher.bot

def start(update, context):
	cht = update.effective_message.chat
	usr = update.effective_user
	msg = update.effective_message
	
	if cht.type == "private":
		if "help" in msg.text:
			msg.reply_text(
				"""
help
				""".format(user.first_name), parse_mode="HTML")
		else:
			msg.reply_text("""
start
			""")
	else:
		msg.reply_text(START_STRING2[CHAT_LANGS[cid]])

def help(update, context):
	cht = update.effective_message.chat
	usr = update.effective_user
	msg = update.effective_message
	
	if chat.type == "private":
		msg.reply_text("""
help
			""".format(user.first_name), parse_mode="HTML")
	else:
		HELP_REPLY_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("Help", url='http://t.me/{}?start=help_{}'.format(bot.username, CHAT_LANGS[cid]))]])
		msg.reply_text("Click the button to get help in PM!", reply_markup=HELP_REPLY_MARKUP)



START_HANDLER = CommandHandler("start", start)
HELP_HANDLER = CommandHandler("help", help)
