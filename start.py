from bot import dispatcher
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler
from lang_sql import *
from strings import *

bot = dispatcher.bot

START_REPLY_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton(START_STRING3, url='http://t.me/{}?startgroup=botstart'.format(bot.username))]])

LANGS = ("کوردیی ناوەندی ☀️", "English 🇺🇸", "Русский 🇷🇺", "O‘zbek 🇺🇿")
LANGS_KEYBOARD = [[InlineKeyboardButton(LANGS[0], callback_data="ku")],[InlineKeyboardButton(LANGS[1], callback_data="en")],[InlineKeyboardButton(LANGS[2], callback_data="ru")],[InlineKeyboardButton(LANGS[3], callback_data="uz")]]
LANGS_REPLY_MARKUP = InlineKeyboardMarkup(LANGS_KEYBOARD)

def start(update, context):
	chat = update.effective_message.chat
	user = update.effective_user
	msg = update.effective_message
	cid = str(chat.id)
	
	if chat.type == "private":
		if "help" in msg.text:
			msg.reply_text(HELP_STRING.format(user.first_name), parse_mode="HTML")
		else:
			msg.reply_text(START_STRING[CHAT_LANGS[cid]], reply_markup=START_REPLY_MARKUP).reply_text(LANG_STRING[cid], reply_markup=LANGS_REPLY_MARKUP, quote=True)
	else:
		msg.reply_text(START_STRING2[CHAT_LANGS[cid]]).reply_text(LANG_STRING[CHAT_LANGS[cid]], reply_markup=LANGS_REPLY_MARKUP, quote=True)

def help(update, context):
	chat = update.effective_message.chat
	user = update.effective_user
	msg = update.effective_message
	cid = str(chat.id)
	
	if chat.type == "private":
		msg.reply_text(HELP_STRING.format(user.first_name), parse_mode="HTML")
	else:
		HELP_REPLY_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton(HELP_STRING3[CHAT_LANGS[cid]], url='http://t.me/{}?start=help'.format(bot.username))]])
		msg.reply_text(HELP_STRING2[CHAT_LANGS[cid]], reply_markup=HELP_REPLY_MARKUP)

def button(update, context):
	query = update.callback_query
	query.answer()
	query.message.reply_to_message.delete()
	
	set_lang(str(query.message.chat.id), query.data)
	
	STRINGS = {"ku": "زمانی ئەم چاتە کرا بە کوردی.", "en": "The language of this chat was set to English.", "ru": "Я буду говорить по Русски.", "uz": "Men bundan buyon O‘zbek tilida gaplashaman."}
	query.edit_message_text(STRINGS[query.data])

START_HANDLER = CommandHandler("start", start)
HELP_HANDLER = CommandHandler("help", help)
BTN_HANDLER = CallbackQueryHandler(button)
