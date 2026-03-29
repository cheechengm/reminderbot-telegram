from database.database import reminders

async def delete_reminder(update, context):
    user_id = update.message.chat_id

    try:
        index = int(context.args[0]) - 1
    except:
        await update.message.reply_text("Usage: /delete <number>")
        return

    user_reminders = list(reminders.find({"user_id": user_id}))

    if index < 0 or index >= len(user_reminders):
        await update.message.reply_text("Invalid number ❌")
        return

    reminders.delete_one({"_id": user_reminders[index]["_id"]})

    await update.message.reply_text("Deleted ✅")