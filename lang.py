from telegram.ext import CommandHandler, CallbackQueryHandler

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from strings import get_languages, get_string

def language_buttons(languages):
	buttons = []
	
	for language in languages:
		buttons.append(InlineKeyboardButton(languages[language], callback_data=f"chatlang_{language}"))
	
	menu = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
	
	return menu

def change_language(update, context):
	chat_data, lang = context.chat_data, None
	
	if "lang" not in chat_data:
		chat_data["lang"] = "en"
	
	lang = chat_data["lang"]
	
	cht, usr, msg = update.effective_chat, update.effective_user, update.effective_message
	
	languages = get_languages()
	buttons = language_buttons(languages)
	msg.reply_text(get_string(lang, "clanguage"), reply_markup=InlineKeyboardMarkup(buttons))

def selected_language(update, context):
	query = update.callback_query
	
	if query.message.chat.type != "private":
		if query.message.chat.get_member(query.from_user.id).status not in ("creator", "administrator"):
			query.answer("You're not an admin in this chat. :(", show_alert=True)
			return
	
	data = query.data.split("_")
	selected_lang = data[1]
	context.chat_data["lang"] = selected_lang
	
	query.edit_message_text(get_string(selected_lang, "languagec"))

CHANGE_LANGUAGE_HANDLER = CommandHandler("lang", change_language)
SELECT_LANGUAGE_HANDLER = CallbackQueryHandler(selected_language)
