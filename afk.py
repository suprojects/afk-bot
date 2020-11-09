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
import threading

AFK_GROUP = 1
AFK_REPLY_GROUP = 2
NO_AFK_GROUP = 1

bot = dispatcher.bot

TEMP_CHANNEL_ID = -1001472428252

def delm(m):
	return m.delete()

def afk(update, context):
	chat = update.effective_message.chat
	cid = str(chat.id)
	init(cid)
	args = update.effective_message.text.split(None, 1)
	if len(args) >= 2:
		reason = args[1]
	else:
		reason = ""
	
	sql.set_afk(update.effective_user.id, reason)
	update.effective_message.reply_text(NOW_AFK[CHAT_LANGS[cid]].format(update.effective_user.first_name))



def no_longer_afk(update, context):
	chat = update.effective_message.chat
	cid = str(chat.id)
	init(cid)
	user = update.effective_user  # type: Optional[User]

	if not user:  # ignore channels
		return
	
	res = sql.rm_afk(user.id)
	if res:
		update.effective_message.reply_text(NOL_AFK[CHAT_LANGS[cid]].format(update.effective_user.first_name))

def reply_afk(update, context):
	chat = update.effective_message.chat
	cid = str(chat.id)
	init(cid)
	message = update.effective_message  # type: Optional[Message]
	entities = message.parse_entities([MessageEntity.TEXT_MENTION, MessageEntity.MENTION])
	user_id = False
	if message.entities and entities:
		for ent in entities:
			if ent.type == MessageEntity.TEXT_MENTION:
				user_id = ent.user.id
				fst_name = ent.user.first_name
			elif ent.type == MessageEntity.MENTION:
				user_id = get_user_id(message.text[ent.offset:ent.offset + ent.length])
				if not user_id:
					return
				chat = bot.get_chat(user_id)
				fst_name = chat.first_name
			else:
				return
	elif bool(message.reply_to_message):
		fst_name = message.reply_to_message.from_user.first_name
		user_id = message.reply_to_message.from_user.id
	
	if user_id:
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
						m=message.reply_photo(context.chat_data[chat.id], caption=res)
					except:
						try:
							m=message.reply_video(context.chat_data[chat.id], caption=res)
						except:
							try:
								m=message.reply_document(context.chat_data[chat.id], caption=res)
							except:
								m=message.reply_text(res)
				threading.Timer(300, delm, [m]).start()

def afkrm(update, context):
	chat = update.effective_message.chat
	cid = str(chat.id)
	init(cid)
	message = update.effective_message
	reply = message.reply_to_message
	
	if bool(reply):
		if bool(reply.photo):
			context.chat_data[chat.id] = reply.photo[-1].file_id
		elif bool(reply.video):
			context.chat_data[chat.id] = reply.video.file_id
		elif bool(reply.document):
			if reply.document.mime_type == "video/mp4":
				context.chat_data[chat.id] = reply.document.file_id
	
	if chat.id in context.chat_data:
		message.reply_text("OK. This will be used.")
	else:
		message.reply_text("Please reply a media.")
		

AFK_HANDLER = CommandHandler("afk", afk)
AFK_MEDIA_HANDLER = CommandHandler("afk_reply_media", afkrm)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.group, no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all, reply_afk)
