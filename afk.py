from typing import Optional

from telegram import Message, Update, User
from telegram import MessageEntity
from telegram.ext import Filters, CommandHandler, MessageHandler
from bot import dispatcher
import afk_sql as sql
from users import get_user_id
from lang_sql import *
from strings import *
from datetime import datetime
from config import Config as c
import threading

AFK_GROUP = 1
AFK_REPLY_GROUP = 2
NO_AFK_GROUP = 1

bot = dispatcher.bot

SUDO_USERS = c.SUDO_USERS

def delm(m):
	return m.delete()

def afk(update, context):
	usr, msg = update.effective_user, update.effective_message
	init(str(cht.id))
	
	args = msg.text.split(None, 1)
	
	if len(args) >= 2:
		reason = args[1]
	else:
		reason = ""
	
	sql.set_afk(usr.id, reason)
	msg.reply_text("{} is now AFK!".format(usr.first_name))



def no_longer_afk(update, context):
	cht = update.effective_chat
	usr = update.effective_user
	msg = update.effective_message
	init(str(cht.id))
	
	if not usr:
		return
	
	res = sql.rm_afk(usr.id)
	if res:
		msg.reply_text("{} is no longer AFK!".format(usr.first_name))

def reply_afk(update, context):
	cht = update.effective_chat
	usr = update.effective_user
	msg = update.effective_message
	init(str(cht.id))
	
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
				chat = bot.get_chat(user_id)
				fst_name = chat.first_name
			else:
				return
	elif bool(msg.reply_to_message):
		fst_name = msg.reply_to_message.from_user.first_name
		user_id = msg.reply_to_message.from_user.id
	
	if bool(user_id):
		if sql.is_afk(user_id):
			valid, reason, since = sql.check_afk_status(user_id)
			
			if valid:
				since = datetime.utcnow() - since
				since = int(since.total_seconds())
				h = since // 3600
				since %= 3600
				m = since // 60
				since %= 60
				since = f"{h} hour(s), {m} minute(s) and {since} second(s)"
				
				if not reason:
					res = AFK[CHAT_LANGS[cid]].format(fst_name, since)
				else:
					res = AFK2[CHAT_LANGS[cid]].format(fst_name, since, reason)
				
				if chat.id in context.chat_data:
					try:
						m = msg.reply_photo(context.user_data[usr.id], caption=res)
					except:
						try:
							m = msg.reply_video(context.user_data[usr.id], caption=res)
						except:
							try:
								m = msg.reply_document(context.user_data[usr.id], caption=res)
							except:
								m = msg.reply_text(res)
				
				threading.Timer(300, delm, [m]).start()

def reply_media(update, context):
	usr, msg, rep = update.effective_user, update.effective_message, msg.reply_to_message
	init(str(cht.id))
	
	if bool(rep):
		if bool(rep.photo):
			context.user_data[usr.id] = rep.photo[-1].file_id
		elif bool(rep.video):
			context.user_data[usr.id] = rep.video.file_id
		elif bool(rep.document):
			if rep.document.mime_type == "video/mp4":
				context.user_data[usr.id] = rep.document.file_id
	
	if usr.id in context.user_data:
		msg.reply_text("This media will be used in your AFK replies.")
	else:
		msg.reply_text("Please reply a media.")

def reply_media_off(update, context):
	usr, msg = update.effective_user, update.effective_message
	
	try:
		del context.user_data[usr.id]
	except:
		pass
	
	msg.reply_text("No media will be included in your AFK replies.")

AFK_HANDLER = CommandHandler("afk", afk)
AFK_MEDIA_HANDLER = CommandHandler("reply_media", reply_media)
AFK_MEDIA_OFF_HANDLER = CommandHandler("reply_media_off", reply_media_off)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.group, no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all, reply_afk)
