from typing import Optional

from telegram import Message, Update, User
from telegram import MessageEntity
from telegram.ext import Filters, CommandHandler, MessageHandler
from bot import dispatcher
import afk_sql as sql
from users import get_user_id

AFK_GROUP = 1
AFK_REPLY_GROUP = 2
NO_AFK_GROUP = 1

bot = dispatcher.bot

def afk(update, context):
	args = update.effective_message.text.split(None, 1)
	if len(args) >= 2:
		reason = args[1]
	else:
		reason = ""

	sql.set_afk(update.effective_user.id, reason)
	update.effective_message.reply_text("{} is now AFK!".format(update.effective_user.first_name))



def no_longer_afk(update, context):
	user = update.effective_user  # type: Optional[User]

	if not user:  # ignore channels
		return
	print(sql.AFK_USERS)
	res = sql.rm_afk(user.id)
	if res:
		update.effective_message.reply_text("{} is no longer AFK!".format(update.effective_user.first_name))

def reply_afk(update, context):
	message = update.effective_message  # type: Optional[Message]
	entities = message.parse_entities([MessageEntity.TEXT_MENTION, MessageEntity.MENTION])
	user_id = False
	print(sql.AFK_USERS)
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
			valid, reason = sql.check_afk_status(user_id)
			if valid:
				if not reason:
					res = "{} is AFK!".format(fst_name)
				else:
					res = "{} is AFK!\n\nReason:\n{}".format(fst_name, reason)
				message.reply_text(res)

AFK_HANDLER = CommandHandler("afk", afk)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.group, no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all, reply_afk)
