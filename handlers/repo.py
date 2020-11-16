from telegram.ext import CommandHandler, Filters
from config import Config

def repo(update, context, lang):
   update.message.reply_text("https://github.com/rojserbest/afk-tgbot")
   
__handlers__ = [[CommandHandler("repo", repo, filters=Filters.user(Config.SUDO_USERS) & Filters.private)]]
