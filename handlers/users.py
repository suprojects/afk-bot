from io import BytesIO
from time import sleep
from typing import Optional

from telegram import InputMediaPhoto, Chat, Message
from telegram import Update, Bot
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler

from sql import users_sql as sql
from bot import dp, SUDO_USERS

USERS_GROUP = 3

FTS = []


def get_user_id(username):
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
                userdat = dp.bot.get_chat(user_obj.user_id)
                if userdat.username == username:
                    return userdat.id

            except BadRequest as excp:
                if excp.message == 'Chat not found':
                    pass
                else:
                    print("Error extracting user ID")

    return None


def add_photo(update, context):
    global FTS
    msg = update.effective_message
    photo = msg.reply_to_message.photo[-1].file_id
    caption = msg.reply_to_message.caption_html

    FTS.append(InputMediaPhoto(
        media=photo, caption=caption, parse_mode="HTML"))


def broadcast(update, context):
    global FTS
    msg = update.effective_message

    chats = sql.get_all_chats() or []

    for chat in chats:
        try:
            context.bot.send_media_group(int(chat.chat_id), FTS)
            sleep(0.5)
        except:
            pass
    FTS = []
    msg.reply_text("Broadcast complete.")


def log_user(update, context):
    chat = update.effective_chat
    msg = update.effective_message

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


__handlers__ = [
    [CommandHandler("af", add_photo, filters=Filters.user(SUDO_USERS))],
    [CommandHandler("broadcast", broadcast, filters=Filters.user(SUDO_USERS))],
    [MessageHandler(Filters.all & Filters.group, log_user), 7],
    [CommandHandler("chatlist", chats, filters=Filters.user(SUDO_USERS))]
]
