from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler

HELP = """If you send this in a group which I’m in before going AFK:
	<pre>/afk [reason]</pre>
Then if someone mentions or replies you, they’ll be replied like this:
	{} is AFK since [time]!
	
	Reason:
	[reason]

And if you’d like to include a media in your AFK replies, reply a media (photo, gif or video) with this <pre>/reply_media</pre> to include it, to remove the media just send <pre>/reply_media_off</pre>."""

def start(update, context):
	cht, usr, msg = update.effective_message.chat, update.effective_user, update.effective_message
	
	if cht.type == "private":
		if "help" in msg.text:
			msg.reply_text(HELP.format(usr.first_name), parse_mode="HTML")
		else:
			msg.reply_text("""Hello! I’m a simple AFK bot to tell others in a group that you’re (A)way (F)rom (K)eyboard, since when and the reason with some customization if you have specified one whenever they mention or reply you. Send /help to know how to use me.

You can add me to your group as a normal member to start using me.""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("+ Add Me To Your Group +", url="http://t.me/{}?startgroup=botstart".format(context.bot.username))]]))
	else:
		msg.reply_text("Hey there! I'm alive.")

def help(update, context):
	cht, usr, msg = update.effective_message.chat, update.effective_user, update.effective_message
	
	if cht.type == "private":
		msg.reply_text(HELP.format(usr.first_name), parse_mode="HTML")
	else:
		HELP_REPLY_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("Help", url="http://t.me/{}?start=help".format(context.bot.username))]])
		msg.reply_text("Click the button to get help in PM!", reply_markup=HELP_REPLY_MARKUP)



START_HANDLER = CommandHandler("start", start)
HELP_HANDLER = CommandHandler("help", help)
