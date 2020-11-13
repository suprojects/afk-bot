from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler
from strings import get_string

def start(update, context):
	chat_data, lang = context.chat_data, None
	
	if "lang" not in chat_data:
		chat_data["lang"] = "en"
	
	lang = chat_data["lang"]
	
	cht, usr, msg = update.effective_message.chat, update.effective_user, update.effective_message
	
	if cht.type == "private":
		if "help" in msg.text:
			msg.reply_text(get_string(lang, "help").format(usr.first_name), parse_mode="HTML")
		else:
			msg.reply_text(get_string(lang, "start"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_string(lang, "add_me"), url="http://t.me/{}?startgroup=botstart".format(context.bot.username))]]), parse_mode="HTML")
	else:
		msg.reply_text(get_string(lang, "alive"))

def help(update, context):
	chat_data, lang = context.chat_data, None
	
	if "lang" not in chat_data:
		chat_data["lang"] = "en"
	
	lang = chat_data["lang"]
	
	cht, usr, msg = update.effective_message.chat, update.effective_user, update.effective_message
	
	if cht.type == "private":
		msg.reply_text(get_string(lang, "help").format(usr.first_name), parse_mode="HTML")
	else:
		HELP_REPLY_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton(get_string(lang, "help_word"), url="http://t.me/{}?start=help".format(context.bot.username))]])
		msg.reply_text(get_string(lang, "help_pm"), reply_markup=HELP_REPLY_MARKUP)

START_HANDLER = CommandHandler("start", start)
HELP_HANDLER = CommandHandler("help", help)
