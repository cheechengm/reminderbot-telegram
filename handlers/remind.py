from datetime import datetime, timedelta
from database.database import reminders

async def remind(update, context):
    try:
        user_id = update.message.chat_id
        time_input = context.args[0]
        message = " ".join(context.args[1:])
        
        # 1. Get current time in Singapore (UTC + 8)
        # We use utcnow() + 8 hours to stay independent of server settings
        now_sg = datetime.utcnow() + timedelta(hours=8)

        if ":" in time_input:
            # Parse HH:MM
            target_time = datetime.strptime(time_input, "%H:%M").time()
            # Create the reminder time based on TODAY'S date in Singapore
            remind_time_sg = datetime.combine(now_sg.date(), target_time)
            
            # If the time has already passed today, set it for tomorrow
            if remind_time_sg < now_sg:
                remind_time_sg += timedelta(days=1)
        else:
            # Handle minutes
            minutes = int(time_input)
            remind_time_sg = now_sg + timedelta(minutes=minutes)

        # 2. CONVERT TO UTC FOR DATABASE
        # This matches the 'datetime.now()' used in your reminder loop
        remind_at_utc = remind_time_sg - timedelta(hours=8)

        reminders.insert_one({
            "user_id": user_id,
            "message": message,
            "remind_at": remind_at_utc
        })

        # Show the user the Singapore time so they aren't confused
        readable_time = remind_time_sg.strftime("%H:%M")
        await update.message.reply_text(f"⏰ Reminder set for {readable_time} SGT!")

    except Exception as e:
        print(f"Error in remind handler: {e}")
        await update.message.reply_text("Usage: /remind <minutes OR HH:MM> <message>")