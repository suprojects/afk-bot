def il(func):  # il = initialize lang :)
    def wrapper(update, context):
        return func(update, context, context.chat_data.get("lang", "en"))
    return wrapper
