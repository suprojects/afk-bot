from telegram.ext import CommandHandler, Filters
from sql.users_sql import get_all_chats, del_chat
import config


def clean(update, context):
    chats = [chat.id for chat in get_all_chats()]
    
    for chat in chats:
        try:
            context.bot.get_chat(chat)
        except:
            try:
                del_chat(chat)
            except:
                pass
    update.message.reply_text("Database cleaning finished.")


__handlers__ = [
    [CommandHandler("clean", clean, filters=Filters.user(config.Config.SUDO_USERS))]
]
