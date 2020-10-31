from bot import dispatcher
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler
bot = dispatcher.bot
START_STRING = """
Hello! I’m a simple AFK bot to tell others in a group that you’re (A)way (F)rom (K)eyboard whenever they mention you or reply you. Send /help to know how to use me.

You can add me to your group as a normal member to start using me.
"""
START_STRING2 = "Hey there! I’m alive."
START_STRING3 = "+ Add Me To Your Group +"
START_REPLY_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton(START_STRING3, url='http://t.me/{}?startgroup=botstart'.format(bot.username))]])

HELP_STRING = """
If you send this in a group which I am in before going AFK:
	<pre>/afk [reason]</pre>

And then someone mentions or replies you, they’ll be replied like this:
	{} is AFK!
	
	Reason:
	[reason]
"""
HELP_STRING2 = """
Click on the button below to get help in PM!
"""
HELP_STRING3 = "Help"
LANG_STRING = "Language"
LANGS = ("کوردیی ناوەندی ☀️", "English 🇺🇸", "Русский 🇷🇺", "O‘zbek 🇺🇿")
LANGS_KEYBOARD = [[InlineKeyboardButton(LANGS[0], callback_data="ku")],[InlineKeyboardButton(LANGS[1], callback_data="en")],[InlineKeyboardButton(LANGS[2], callback_data="ru")],[InlineKeyboardButton(LANGS[3], callback_data="uz")]]
LANGS_REPLY_MARKUP = InlineKeyboardMarkup(LANGS_KEYBOARD)

HELP_REPLY_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton(HELP_STRING3, url='http://t.me/{}?start=help'.format(bot.username))]])

def start(update, context):
	chat = update.effective_message.chat
	user = update.effective_user
	msg = update.effective_message
	
	if chat.type == "private":
		if "help" in msg.text:
			msg.reply_text(HELP_STRING.format(user.first_name), parse_mode="HTML")
		else:
			msg.reply_text(START_STRING, reply_markup=START_REPLY_MARKUP).reply_text(LANG_STRING, reply_markup=LANGS_REPLY_MARKUP, quote=True)
	else:
		msg.reply_text(START_STRING2).reply_text(LANG_STRING, reply_markup=LANGS_REPLY_MARKUP, quote=True)

def help(update, context):
	chat = update.effective_message.chat
	user = update.effective_user
	msg = update.effective_message
	
	if chat.type == "private":
		msg.reply_text(HELP_STRING.format(user.first_name), parse_mode="HTML")
	else:
		msg.reply_text(HELP_STRING2, reply_markup=HELP_REPLY_MARKUP)

START_HANDLER = CommandHandler("start", start)
HELP_HANDLER = CommandHandler("help", help)
