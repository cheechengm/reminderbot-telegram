from database.database import reminders

async def list_reminders(update, context):
    user_id = update.message.chat_id

    user_reminders = list(reminders.find({"user_id": user_id}))

    if not user_reminders:
        await update.message.reply_text("No reminders 😢")
        return

    text = "📋 Your reminders:\n\n"

    for i, r in enumerate(user_reminders, start=1):
        text += f"{i}. {r['message']}\n"

    await update.message.reply_text(text)