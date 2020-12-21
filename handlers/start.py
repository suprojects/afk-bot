from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler
from strings import get_string
from il import il


@il
def start(update, context, lang):
    cht, usr, msg = update.effective_message.chat, update.effective_user, update.effective_message

    if cht.type == "private":
        if "help" in msg.text:
            msg.reply_text(get_string(lang, "help").format(
                usr.first_name), parse_mode="HTML")
        else:
            msg.reply_text(get_string(lang, "start"),
                           reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            get_string(
                                lang,
                                "add_me"
                            ),
                            url=f"http://t.me/{}?startgroup=lang_{lang}".format(
                                context.bot.username)
                        )
                    ]
                ]
            ),
                parse_mode="HTML")
    else:
        if "lang" in msg.text:
            lang = msg.text.split("_")[-1]
            context.bot_dat["lang"] = lang
            
        msg.reply_text(get_string(lang, "alive"))


@il
def help(update, context, lang):
    chat_data, lang = context.chat_data, None

    if "lang" not in chat_data:
        chat_data["lang"] = "en"

    lang = chat_data["lang"]

    cht, usr, msg = update.effective_message.chat, update.effective_user, update.effective_message

    if cht.type == "private":
        msg.reply_text(get_string(lang, "help").format(
            usr.first_name), parse_mode="HTML")
    else:
        HELP_REPLY_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton(get_string(
            lang, "help_word"), url="http://t.me/{}?start=help".format(context.bot.username))]])
        msg.reply_text(get_string(lang, "help_pm"),
                       reply_markup=HELP_REPLY_MARKUP)


__handlers__ = [
    [CommandHandler("start", start)],
    [CommandHandler("help", help)]
]
