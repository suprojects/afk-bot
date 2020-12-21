import threading

from sqlalchemy import Column, Integer, UnicodeText, String

from bot import dp
from sql import BASE, SESSION


class Users(BASE):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(UnicodeText)

    def __init__(self, user_id, username=None):
        self.user_id = user_id
        self.username = username


class Chats(BASE):
    __tablename__ = "chats"
    chat_id = Column(String(14), primary_key=True)
    chat_name = Column(UnicodeText, nullable=False)

    def __init__(self, chat_id, chat_name):
        self.chat_id = str(chat_id)
        self.chat_name = chat_name


Users.__table__.create(checkfirst=True)
Chats.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def ensure_bot_in_db():
    with INSERTION_LOCK:
        bot = Users(dp.bot.id, dp.bot.username)
        SESSION.merge(bot)
        SESSION.commit()


def update_user(user_id, username, chat_id=None, chat_name=None):
    with INSERTION_LOCK:
        user = SESSION.query(Users).get(user_id)
        if not user:
            user = Users(user_id, username)
            SESSION.add(user)
            SESSION.flush()
        else:
            user.username = username

        if not chat_id or not chat_name:
            SESSION.commit()
            return

        chat = SESSION.query(Chats).get(str(chat_id))
        if not chat:
            chat = Chats(str(chat_id), chat_name)
            SESSION.add(chat)
            SESSION.flush()

        else:
            chat.chat_name = chat_name

        SESSION.commit()


def get_userid_by_name(username):
    try:
        return SESSION.query(Users).filter(func.lower(Users.username) == username.lower()).all()
    finally:
        SESSION.close()


def get_name_by_userid(user_id):
    try:
        return SESSION.query(Users).get(Users.user_id == int(user_id)).first()
    finally:
        SESSION.close()


def get_all_chats():
    try:
        return SESSION.query(Chats).all()
    finally:
        SESSION.close()


def num_chats():
    try:
        return SESSION.query(Chats).count()
    finally:
        SESSION.close()


def num_users():
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()


ensure_bot_in_db()


def del_user(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(Users).get(user_id)
        if curr:
            SESSION.delete(curr)
            SESSION.commit()
            return True

        SESSION.commit()
        SESSION.close()
    return False


def del_chat(chat_id):
    with INSERTION_LOCK:
        curr = SESSION.query(Chats).get(chat_id)
        if curr:
            SESSION.delete(curr)
            SESSION.commit()
            return True

        SESSION.commit()
        SESSION.close()
    return False
