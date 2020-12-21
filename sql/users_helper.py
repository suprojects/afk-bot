from telegram.error import BadRequest

from bot import dp
import sql.users_sql as sql


def chats(wname=False):
    if not wname:
        return [
            chat.chat_id for chat in sql.get_all_chats()
        ]
    else:
        return [
            chat for chat in sql.get_all_chats()
        ]


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
                if excp.message == "Chat not found":
                    pass
                else:
                    print("Error extracting user ID")

    return None
