from sqlalchemy import String, Column

from sql import BASE, SESSION


class Lang(BASE):
	__tablename__ = "chat_langs"

	chat_id = Column(String, primary_key=True)
	lang = Column(String)
	
	def __init__(self, chat_id, lang="en"):
		self.chat_id = chat_id
		self.lang = lang

Lang.__table__.create(checkfirst=True)

CHAT_LANGS = {}

def is_selected(chat_id):
	return chat_id in CHAT_LANGS

def get_selected(chat_id):
	return CHAT_LANGS[chat_id]

def init(chat_id):
	if not is_selected(chat_id):
		CHAT_LANGS[chat_id] = "en"

def set_lang(chat_id, lang="en"):
	try:
		curr = SESSION.query(Lang).get(chat_id)
		if not curr:
			curr = Lang(chat_id, lang)
		else:
			curr.lang = lang
		CHAT_LANGS[chat_id] = lang
		SESSION.add(curr)
		SESSION.commit()
	except:
		SESSION.rollback()
		raise

def __load_user_langs():
	global CHAT_LANGS
	try:
		all_langs = SESSION.query(Lang).all()
		CHAT_LANGS = {lang.chat_id: lang.lang for lang in all_langs}
	finally:
		SESSION.close()

__load_user_langs()
