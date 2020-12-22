from sql.users_sql import del_chat
from secrets import LOG_CHAT


def error(update, context):
    chat, usr = update.effective_chat, update.effective_user

    context.bot.send_message(
        LOG_CHAT, """
#{}

Chat ID: {}
User ID: {}

Error:
{}
""".format(
            context.bot.username,
            chat.id,
            usr.id,
            context.error
        )
    )

    try:
        if context.error.message == "Have no rights to send a message":
            chat.leave()
            del_chat(chat.id)
        else:
            update.message.reply_text(
                "An unexpected error occured.\n"
                "Logs were sent to developers."
            )
    except:
        pass


__handlers__ = [
    [
        "error",
        error
    ]
]
