async def start(update, context):
    await update.message.reply_text(
        "Hello! ⏰\n\n"
        "/remind 1 test\n"
        "/list\n"
        "/delete 1\n"
    )