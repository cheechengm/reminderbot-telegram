from datetime import datetime, timedelta
from database.database import reminders

async def remind(update, context):
    try:
        user_id = update.message.chat_id

        minutes = int(context.args[0])
        message = " ".join(context.args[1:])

        remind_time = datetime.now() + timedelta(minutes=minutes)

        reminders.insert_one({
            "user_id": user_id,
            "message": message,
            "remind_at": remind_time
        })

        await update.message.reply_text("⏰ Reminder set!")

    except:
        await update.message.reply_text("Usage: /remind <minutes> <message>")