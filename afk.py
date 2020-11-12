import threading
from datetime import datetime

from telegram import Message, Update, User
from telegram import MessageEntity
from telegram.ext import Filters, CommandHandler, MessageHandler

import afk_sql as sql
from users import get_user_id

from strings import get_string

AFK_GROUP = 1
AFK_REPLY_GROUP = 2
NO_AFK_GROUP = 1

def delm(m):
	return m.delete()

def afk(update, context):
	chat_data, lang = context.chat_data, None
	
	if "lang" not in chat_data:
		chat_data["lang"] = "en"
	
	lang = chat_data["lang"]
	
	usr, msg = update.effective_user, update.effective_message
	rep = msg.reply_to_message
	
	try:
		del context.bot_data[usr.id]
	except:
		pass
	
	if bool(rep):
		if bool(rep.photo):
			context.bot_data[usr.id] = rep.photo[-1].file_id
		elif bool(rep.video):
			context.bot_data[usr.id] = rep.video.file_id
		elif bool(rep.document):
			if rep.document.mime_type == "video/mp4":
				context.bot_data[usr.id] = rep.document.file_id
	
	args = msg.text.split(None, 1)
	
	if len(args) >= 2:
		reason = args[1]
	else:
		reason = ""
	
	sql.set_afk(usr.id, reason)
	msg.reply_text(get_string(lang, "now_afk").format(usr.first_name))

def afk2(update, context):
	chat_data, lang = context.chat_data, None
	
	if "lang" not in chat_data:
		chat_data["lang"] = "en"
	
	lang = chat_data["lang"]
	
	usr, msg = update.effective_user, update.effective_message
	
	if not bool(msg.caption):
		return
	
	if not msg.caption.startswith("/afk"):
		return
	
	file_id = msg.video.file_id if bool(msg.video) else msg.photo[-1].file_id
	context.bot_data[usr.id] = file_id
	
	args = msg.caption.split(None, 1)
	
	if len(args) >= 2:
		reason = args[1]
	else:
		reason = ""
	
	sql.set_afk(usr.id, reason)
	msg.reply_text(get_string(lang, "now_afk").format(usr.first_name))

def no_longer_afk(update, context):
	chat_data, lang = context.chat_data, None
	
	if "lang" not in chat_data:
		chat_data["lang"] = "en"
	
	lang = chat_data["lang"]
	
	usr, msg = update.effective_user, update.effective_message
	
	if not usr:
		return
	
	res = sql.rm_afk(usr.id)
	
	if res:
		msg.reply_text(get_string(lang, "nol_afk").format(usr.first_name))

def reply_afk(update, context):
	chat_data, lang = context.chat_data, None
	
	if "lang" not in chat_data:
		chat_data["lang"] = "en"
	
	lang = chat_data["lang"]
	
	cht, usr, msg = update.effective_chat, update.effective_user, update.effective_message
	
	entities = msg.parse_entities([MessageEntity.TEXT_MENTION, MessageEntity.MENTION])
	user_id = None
	
	if msg.entities and entities:
		for ent in entities:
			if ent.type == MessageEntity.TEXT_MENTION:
				user_id = ent.user.id
				fst_name = ent.user.first_name
			elif ent.type == MessageEntity.MENTION:
				user_id = get_user_id(msg.text[ent.offset:ent.offset + ent.length])
				if not user_id:
					return
				fst_name = context.bot.get_chat(user_id).first_name
			else:
				return
	elif bool(msg.reply_to_message):
		fst_name = msg.reply_to_message.from_user.first_name
		user_id = msg.reply_to_message.from_user.id
	
	if bool(user_id):
		if user_id == usr.id:
			return
		if sql.is_afk(user_id):
			valid, reason, since = sql.check_afk_status(user_id)
			
			if valid:
				since = datetime.utcnow() - since
				since = int(since.total_seconds())
				h = since // 3600
				since %= 3600
				m = since // 60
				since %= 60
				since = get_string(lang, "since").format(h, m, since)
				
				if not reason:
					res = "{}\n{}.".format(get_string(lang, "afk").format(fst_name), since)
				else:
					res = "{} is AFK. \n{}\n\n{}".format(get_string(lang, "afk").format(fst_name), since, get_string(lang, "reason").format(reason))
				
				m = False
				
				try:
					m = msg.reply_photo(context.bot_data[user_id], caption=res)
				except:
					m = False
				
				try:
					if not m:
						m = msg.reply_video(context.bot_data[user_id], caption=res)
				except:
					m = False
				
				try:
					if not m:
						m = msg.reply_document(context.bot_data[user_id], caption=res)
				except:
					m = False
				
				
				if not m:
					m = msg.reply_text(res)
				
				threading.Timer(300, delm, [m]).start()

AFK_HANDLER = CommandHandler("afk", afk)
AFK2_HANDLER = MessageHandler(Filters.photo | Filters.video, afk2)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.group, no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all, reply_afk)
