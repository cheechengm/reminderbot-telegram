import re
from datetime import datetime, timedelta
from database.database import reminders

async def remind(update, context):
    try:
        user_id = update.message.chat_id
        args = context.args
        
        if len(args) < 2:
            raise ValueError("Missing arguments")

        time_input = args[0]
        # Check if the second argument is a time (making the first a date)
        # e.g., /remind 31/03 10:00 message
        if len(args) > 2 and (":" in args[1] or (args[1].isdigit() and len(args[1]) <= 4)):
            date_input = args[0]
            time_input = args[1]
            message = " ".join(args[2:])
        else:
            date_input = None
            message = " ".join(args[1:])

        # 1. Get Singapore Time (UTC + 8)
        now_sg = datetime.utcnow() + timedelta(hours=8)
        remind_time_sg = None

        # 2. Parse Time (HH:MM or HHMM)
        time_match = re.match(r"^(\d{1,2}):?(\d{2})$", time_input)
        
        if time_match:
            hours = int(time_match.group(1))
            minutes = int(time_match.group(2))
            
            if date_input:
                # Parse Date (DD/MM or DDMM)
                date_match = re.match(r"^(\d{1,2})/?(\d{2})$", date_input)
                if date_match:
                    day = int(date_match.group(1))
                    month = int(date_match.group(2))
                    # Use current year, set specific date/time
                    remind_time_sg = now_sg.replace(month=month, day=day, hour=hours, minute=minutes, second=0, microsecond=0)
                else:
                    raise ValueError("Invalid date format")
            else:
                # No date provided, assume today (or tomorrow if time passed)
                remind_time_sg = now_sg.replace(hour=hours, minute=minutes, second=0, microsecond=0)
                if remind_time_sg < now_sg:
                    remind_time_sg += timedelta(days=1)
        else:
            # 3. Handle as Minutes (only if no date was provided)
            if date_input:
                raise ValueError("Format error")
            minutes_delta = int(time_input)
            remind_time_sg = now_sg + timedelta(minutes=minutes_delta)

        # 4. Save to DB as UTC (Subtract 8 hours)
        remind_at_utc = remind_time_sg - timedelta(hours=8)

        reminders.insert_one({
            "user_id": user_id,
            "message": message,
            "remind_at": remind_at_utc
        })

        # Pretty confirmation
        friendly_date = remind_time_sg.strftime("%d %b, %H:%M")
        await update.message.reply_text(
            f"✅ **Reminder Set!**\n"
            f"📅 Date: `{friendly_date}` SGT\n"
            f"📝 Note: {message}",
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text(
            "❌ **Invalid Format**\n\n"
            "Try these:\n"
            "• `/remind 10 buy milk` (10 mins)\n"
            "• `/remind 19:30 call mom` (Tonight)\n"
            "• `/remind 31/03 09:00 meeting` (Specific date)",
            parse_mode="Markdown"
        )