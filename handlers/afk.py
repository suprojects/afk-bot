from threading import Timer
from datetime import datetime
from telegram import MessageEntity
from telegram.ext import Filters, CommandHandler, MessageHandler

import sql.afk_sql as sql
from sql.users_helper import get_user_id
from strings import get_string
from il import il


def delm(m, r=False):
    if r:
        return m.delete()
    else:
        return Timer(300, delm, [m, True]).start()


@il
def status(update, context, lang):
    usr, msg = update.effective_user, update.effective_message
    valid, reason, since = sql.check_afk_status(usr.id)

    if valid:
        since = datetime.utcnow() - since
        since = int(since.total_seconds())
        h = since // 3600
        since %= 3600
        m = since // 60
        since %= 60
        media = context.bot_data.get(usr.id, False)
        text = get_string(
            lang,
            "status_afk_reason"
        ).format(
            h,
            m,
            since,
            reason
        ) if reason else get_string(
            lang,
            "status_afk"
        ).format(
            h,
            m,
            since
        )

        if text:
            if media:
                try:
                    msg.reply_video(
                        media,
                        caption=text
                    )
                    return
                except:
                    try:
                        msg.reply_photo(
                            media,
                            caption=text
                        )
                        return
                    except:
                        try:
                            msg.reply_document(
                                media,
                                caption=text
                            )
                            return
                        except:
                            return
    else:
        msg.reply_text(
            get_string(
                lang,
                "status_not_afk"
            )
        )


@il
def afk(update, context, lang):
    usr, msg = update.effective_user, update.effective_message
    rep = msg.reply_to_message

    try:
        del context.bot_data[usr.id]
    except:
        pass

    if bool(rep):
        if bool(rep.photo):
            context.bot_data[usr.id] = rep.photo[-1].file_id
        elif bool(rep.video):
            context.bot_data[usr.id] = rep.video.file_id
        elif bool(rep.document):
            if rep.document.mime_type == "video/mp4":
                context.bot_data[usr.id] = rep.document.file_id

    args = msg.text.split(None, 1)

    if len(args) >= 2:
        reason = args[1]
    else:
        reason = ""

    sql.set_afk(usr.id, reason)
    m = msg.reply_text(get_string(lang, "now_afk").format(usr.first_name))
    delm(m)


@il
def afk2(update, context, lang):
    usr, msg = update.effective_user, update.effective_message

    if not bool(msg.caption):
        return

    if not msg.caption.startswith("/afk"):
        return

    file_id = msg.video.file_id if bool(msg.video) else msg.photo[-1].file_id
    context.bot_data[usr.id] = file_id

    args = msg.caption.split(None, 1)

    if len(args) >= 2:
        reason = args[1]
    else:
        reason = ""

    sql.set_afk(usr.id, reason)
    m = msg.reply_text(get_string(lang, "now_afk").format(usr.first_name))
    delm(m)


@il
def no_longer_afk(update, context, lang):
    chat_data, lang = context.chat_data, None

    if "lang" not in chat_data:
        chat_data["lang"] = "en"

    lang = chat_data["lang"]

    usr, msg = update.effective_user, update.effective_message

    if not usr:
        return

    valid, reason, since = sql.check_afk_status(usr.id)

    if valid:
        res = sql.rm_afk(usr.id)
        since = datetime.utcnow() - since
        since = int(since.total_seconds())
        h = since // 3600
        since %= 3600
        m = since // 60
        since %= 60

        if res:
            m = msg.reply_text(
                get_string(
                    lang, "back_online"
                ).format(
                    usr.first_name,
                    h,
                    m,
                    since
                ) + "\n\n" + get_string(
                    lang,
                    "reason"
                ).format(
                    reason
                )
            )
            delm(m)


@il
def reply_afk(update, context, lang):
    usr, msg = update.effective_user, update.effective_message

    entities = msg.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
    )
    user_id = None

    if msg.entities and entities:
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name
            elif ent.type == MessageEntity.MENTION:
                user_id = get_user_id(
                    msg.text[
                        ent.offset:ent.offset + ent.length
                    ]
                )
                if not user_id:
                    return
                fst_name = context.bot.get_chat(user_id).first_name
            else:
                return
    elif bool(msg.reply_to_message):
        fst_name = msg.reply_to_message.from_user.first_name
        user_id = msg.reply_to_message.from_user.id

    if bool(user_id):
        if user_id == usr.id:
            return
        if sql.is_afk(user_id):
            valid, reason, since = sql.check_afk_status(user_id)

            if valid:
                since = datetime.utcnow() - since
                since = int(since.total_seconds())
                h = since // 3600
                since %= 3600
                m = since // 60
                since %= 60
                since = get_string(lang, "since").format(h, m, since)

                if not reason:
                    res = "{}\n{}".format(
                        get_string(
                            lang,
                            "afk"
                        ).format(
                            fst_name
                        ),
                        since
                    )
                else:
                    res = "{}\n{}\n\n{}".format(
                        get_string(
                            lang,
                            "afk"
                        ).format(
                            fst_name
                        ), since, get_string(lang, "reason").format(
                            reason
                        )
                    )

                m = False

                try:
                    m = msg.reply_photo(context.bot_data[user_id], caption=res)
                except:
                    m = False

                try:
                    if not m:
                        m = msg.reply_video(
                            context.bot_data[user_id], caption=res)
                except:
                    m = False

                try:
                    if not m:
                        m = msg.reply_document(
                            context.bot_data[user_id], caption=res)
                except:
                    m = False

                if not m:
                    m = msg.reply_text(res)

                delm(m)


__handlers__ = [
    [
        CommandHandler(
            "afk",
            afk
        ),
        7
    ],
    [
        MessageHandler(
            Filters.photo |
            Filters.video,
            afk2
        ),
        7
    ],
    [
        CommandHandler(
            "status",
            status
        ),
        7
    ],
    [
        MessageHandler(
            (
                Filters.all & ~
                Filters.status_update & ~
                Filters.command
            ) &
            Filters.chat_type.groups,
            no_longer_afk
        ),
        7
    ],
    [
        MessageHandler(
            Filters.all,
            reply_afk
        ),
        8
    ]
]
