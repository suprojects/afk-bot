from sqlalchemy import Column, UnicodeText, Boolean, Integer, DateTime

from sql import BASE, SESSION

from datetime import datetime


class AFK(BASE):
	__tablename__ = "afk_users"

	user_id = Column(Integer, primary_key=True)
	is_afk = Column(Boolean)
	reason = Column(UnicodeText)
	since = Column(DateTime)
	
	def __init__(self, user_id, reason="", is_afk=True, since):
		self.user_id = user_id
		self.reason = reason
		self.is_afk = is_afk
		self.since = since

	def __repr__(self):
		return "afk_status for {}".format(self.user_id)


AFK.__table__.create(checkfirst=True)

AFK_USERS = {}


def is_afk(user_id):
	return user_id in AFK_USERS


def check_afk_status(user_id):
	if user_id in AFK_USERS:
		return True, AFK_USERS[user_id][0], AFK_USERS[user_id][1]
	return False, "", None


def set_afk(user_id, reason=""):
	try:
		curr = SESSION.query(AFK).get(user_id)
		if not curr:
			curr = AFK(user_id, reason, True, datetime.utcnow())
		else:
			curr.is_afk = True
			curr.reason = reason
			curr.since = datetime.utcnow()
		AFK_USERS[user_id] = [reason, curr.since]
		SESSION.add(curr)
		SESSION.commit()
	except:
		SESSION.rollback()
		raise


def rm_afk(user_id):
	curr = SESSION.query(AFK).get(user_id)
	if curr:
		if user_id in AFK_USERS:  # sanity check
			del AFK_USERS[user_id]
			SESSION.delete(curr)
			SESSION.commit()
			return True
	SESSION.close()
	return False

def __load_afk_users():
	global AFK_USERS
	try:
		all_afk = SESSION.query(AFK).all()
		AFK_USERS = {user.user_id: [user.reason, user.since] for user in all_afk if user.is_afk}
	finally:
		SESSION.close()


__load_afk_users()
