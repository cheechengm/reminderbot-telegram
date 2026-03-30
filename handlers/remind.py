import re
from datetime import datetime, timedelta
from database.database import reminders

async def remind(update, context):
    try:
        user_id = update.message.chat_id
        args = context.args
        
        if len(args) < 2:
            raise ValueError("Missing arguments")

        # --- RECURRENCE LOGIC ---
        repeat_type = None
        if args[0].lower() in ["daily", "weekly"]:
            repeat_type = args[0].lower()
            args = args[1:] # Shift args to handle time/message normally
        # ------------------------

        time_input = args[0]
        # Check if the second argument is a time (making the first a date)
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
                date_match = re.match(r"^(\d{1,2})/?(\d{2})$", date_input)
                if date_match:
                    day = int(date_match.group(1))
                    month = int(date_match.group(2))
                    remind_time_sg = now_sg.replace(month=month, day=day, hour=hours, minute=minutes, second=0, microsecond=0)
                    if remind_time_sg < now_sg:
                        remind_time_sg = remind_time_sg.replace(year=now_sg.year + 1)
                else:
                    raise ValueError("Invalid date format")
            else:
                remind_time_sg = now_sg.replace(hour=hours, minute=minutes, second=0, microsecond=0)
                if remind_time_sg < now_sg:
                    remind_time_sg += timedelta(days=1)
        else:
            if date_input:
                raise ValueError("Format error")
            minutes_delta = int(time_input)
            remind_time_sg = now_sg + timedelta(minutes=minutes_delta)

        # 3. Calculate Countdown
        diff = remind_time_sg - now_sg
        days = diff.days
        hours_rem, remainder = divmod(int(diff.total_seconds()), 3600)
        minutes_rem, _ = divmod(remainder, 60)

        if days > 0:
            countdown_text = f"{days}d {hours_rem % 24}h {minutes_rem}m"
        elif hours_rem > 0:
            countdown_text = f"{hours_rem}h {minutes_rem}m"
        else:
            countdown_text = f"{minutes_rem}m"

        # 4. Save to DB with 'repeat' field
        remind_at_utc = remind_time_sg - timedelta(hours=8)
        reminders.insert_one({
            "user_id": user_id,
            "message": message,
            "remind_at": remind_at_utc,
            "repeat": repeat_type  # Added this field
        })

        # 5. Confirmation Message
        repeat_label = f"\n🔁 **Repeat:** `{repeat_type.capitalize()}`" if repeat_type else ""
        friendly_date = remind_time_sg.strftime("%d %b, %H:%M")
        
        await update.message.reply_text(
            f"✅ **Reminder Set!**\n\n"
            f"📅 **Date:** `{friendly_date}` SGT\n"
            f"⏳ **Starts in:** `{countdown_text}`"
            f"{repeat_label}\n"
            f"📝 **Note:** {message}",
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text(
            "❌ **Invalid Format**\n\n"
            "• `/remind 10 buy milk` (Once)\n"
            "• `/remind daily 08:00 gym` (Every day)\n"
            "• `/remind weekly 31/03 10:00 meeting` (Every week)",
            parse_mode="Markdown"
        )