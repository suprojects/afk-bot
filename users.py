from io import BytesIO
from time import sleep
from typing import Optional

from telegram import InputMediaPhoto, Chat, Message
from telegram import Update, Bot
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler

import users_sql as sql
from bot import SUDO_USERS

USERS_GROUP = 3

def get_user_id(username):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith('@'):
        username = username[1:]

    users = sql.get_userid_by_name(username)

    if not users:
        return None

    elif len(users) == 1:
        return users[0].user_id

    else:
        for user_obj in users:
            try:
                userdat = dispatcher.bot.get_chat(user_obj.user_id)
                if userdat.username == username:
                    return userdat.id

            except BadRequest as excp:
                if excp.message == 'Chat not found':
                    pass
                else:
                    LOGGER.exception("Error extracting user ID")

    return None

def add_photo(update, context):
    msg = update.effective_message
    photo = msg.reply_to_message.photo[-1].file_id
    caption = msg.reply_to_message.caption
    
    if "photos" not in context.user_data:
        context.user_data["photos"] = []
    context.user_data["photos"].append(InputMediaPhoto(media=photo,caption=caption))
    

def broadcast(update, context):
    msg = update.effective_message
    
    
   # if len(to_send) >= 2:
     #   chats = sql.get_all_chats() or []
    msg.reply_media_group(context.user_data["photos"])
     #   for chat in chats:
        #    try:
              #  context.bot.send_media_group(context.user_data["photos"])
            #    sleep(0.1)
         #   except:
              #  pass

      #  msg.reply_text("Broadcast complete.")



def log_user(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]

    sql.update_user(msg.from_user.id,
                    msg.from_user.username,
                    chat.id,
                    chat.title)

    if msg.reply_to_message:
        sql.update_user(msg.reply_to_message.from_user.id,
                        msg.reply_to_message.from_user.username,
                        chat.id,
                        chat.title)

    if msg.forward_from:
        sql.update_user(msg.forward_from.id,
                        msg.forward_from.username)



def chats(update, context):
    all_chats = sql.get_all_chats() or []
    chatfile = 'List of chats.\n'
    for chat in all_chats:
        chatfile += "{} - ({})\n".format(chat.chat_name, chat.chat_id)

    with BytesIO(str.encode(chatfile)) as output:
        output.name = "chatlist.txt"
        update.effective_message.reply_document(document=output, filename="chatlist.txt",
                                                caption="Here is the list of chats in my database.")


def __user_info__(user_id):
    if user_id == dispatcher.bot.id:
        return """I've seen them in... Wow. Are they stalking me? They're in all the same places I am... oh. It's me."""
    num_chats = sql.get_user_num_chats(user_id)
    return """I've seen them in <code>{}</code> chats in total.""".format(num_chats)


def __stats__():
    return "{} users, across {} chats".format(sql.num_users(), sql.num_chats())


def __gdpr__(user_id):
    sql.del_user(user_id)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


__help__ = ""  # no help string

__mod_name__ = "Users"

AF_HANDLER = CommandHandler("af", add_photo, filters=Filters.user(SUDO_USERS))
BROADCAST_HANDLER = CommandHandler("broadcast", broadcast, filters=Filters.user(SUDO_USERS))
USER_HANDLER = MessageHandler(Filters.all & Filters.group, log_user)
CHATLIST_HANDLER = CommandHandler("chatlist", chats, filters=Filters.user(SUDO_USERS))
