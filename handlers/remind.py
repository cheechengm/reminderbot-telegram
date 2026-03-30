from datetime import datetime, timedelta
from database.database import reminders

async def remind(update, context):
    try:
        user_id = update.message.chat_id
        time_input = context.args[0]  # This is "5" or "19:02"
        message = " ".join(context.args[1:])
        
        now = datetime.now()

        # 1. Check if user provided a specific clock time (HH:MM)
        if ":" in time_input:
            # Parse the HH:MM string
            target_time = datetime.strptime(time_input, "%H:%M").time()
            # Combine today's date with that time
            remind_time = datetime.combine(now.date(), target_time)
            
            # If 19:02 has already passed today, set it for tomorrow
            if remind_time < now:
                remind_time += timedelta(days=1)
        
        # 2. Otherwise, assume they provided minutes
        else:
            minutes = int(time_input)
            remind_time = now + timedelta(minutes=minutes)

        # Save to Database
        reminders.insert_one({
            "user_id": user_id,
            "message": message,
            "remind_at": remind_time
        })

        readable_time = remind_time.strftime("%H:%M")
        await update.message.reply_text(f"⏰ Reminder set for {readable_time}!")

    except Exception as e:
        print(f"Error in remind handler: {e}")
        await update.message.reply_text("Usage: /remind <minutes OR HH:MM> <message>")