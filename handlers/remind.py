import re
from datetime import datetime, timedelta
from database.database import reminders

# Helper to map day names to Python weekday numbers (Monday=0, Sunday=6)
DAYS_MAP = {
    'mon': 0, 'monday': 0, 'tue': 1, 'tuesday': 1, 'wed': 2, 'wednesday': 2,
    'thu': 3, 'thursday': 3, 'fri': 4, 'friday': 4, 'sat': 5, 'saturday': 5,
    'sun': 6, 'sunday': 6
}

async def remind(update, context):
    try:
        user_id = update.message.chat_id
        args = context.args
        
        if not args or len(args) < 2:
            raise ValueError("Insufficient arguments")

        # 1. Handle Recurrence Keyword (daily/weekly)
        repeat_type = None
        if args[0].lower() in ["daily", "weekly"]:
            repeat_type = args[0].lower()
            args = args[1:] 

        time_input = args[0]
        date_input = None
        target_weekday = None

        # 2. Smart Parsing: Check for Day Names (e.g., Sunday)
        if repeat_type == "weekly" and len(args) > 1 and args[1].lower() in DAYS_MAP:
            target_weekday = DAYS_MAP[args[1].lower()]
            message = " ".join(args[2:])
        # Check for Date Input (DD/MM)
        elif len(args) > 2 and (":" in args[1] or (args[1].isdigit() and len(args[1]) <= 4)):
            date_input = args[0]
            time_input = args[1]
            message = " ".join(args[2:])
        else:
            message = " ".join(args[1:])

        # 3. Singapore Time Setup (UTC+8)
        now_sg = datetime.utcnow() + timedelta(hours=8)
        remind_time_sg = None

        # 4. Parse Time (HH:MM or HHMM)
        if time_match := re.match(r"^(\d{1,2}):?(\d{2})$", time_input):
            hours = int(time_match.group(1))
            minutes = int(time_match.group(2))
            
            # Base time for today
            remind_time_sg = now_sg.replace(hour=hours, minute=minutes, second=0, microsecond=0)
            
            if target_weekday is not None:
                # Calculate the next specific day (e.g., next Sunday)
                days_ahead = target_weekday - now_sg.weekday()
                if days_ahead < 0 or (days_ahead == 0 and remind_time_sg < now_sg):
                    days_ahead += 7
                remind_time_sg += timedelta(days=days_ahead)
                
            elif date_input:
                # Parse DD/MM date
                date_match = re.match(r"^(\d{1,2})/?(\d{2})$", date_input)
                if date_match:
                    day, month = int(date_match.group(1)), int(date_match.group(2))
                    remind_time_sg = remind_time_sg.replace(month=month, day=day)
                    if remind_time_sg < now_sg:
                        remind_time_sg = remind_time_sg.replace(year=now_sg.year + 1)
                else:
                    raise ValueError("Invalid date")
            else:
                # If time has already passed today, set for tomorrow
                if remind_time_sg < now_sg:
                    remind_time_sg += timedelta(days=1)
        else:
            # Handle "In X minutes" format
            minutes_delta = int(time_input)
            remind_time_sg = now_sg + timedelta(minutes=minutes_delta)

        # 5. Calculate Countdown for UI
        diff = remind_time_sg - now_sg
        days, remainder = divmod(int(diff.total_seconds()), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)

        if days > 0:
            countdown_text = f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            countdown_text = f"{hours}h {minutes}m"
        else:
            countdown_text = f"{minutes}m"

        # 6. Save to Database (Stored in UTC)
        remind_at_utc = remind_time_sg - timedelta(hours=8)
        reminders.insert_one({
            "user_id": user_id,
            "message": message,
            "remind_at": remind_at_utc,
            "repeat": repeat_type 
        })

        # 7. Success Confirmation Message
        friendly_date = remind_time_sg.strftime("%a, %d %b %H:%M")
        repeat_label = f"\n🔁 **Repeat:** `{repeat_type.capitalize()}`" if repeat_type else ""
        
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
        # categorized Help Exception
        help_text = (
            "❌ **Invalid Format!**\n\n"
            "Try one of these:\n"
            "• `/remind 10 buy milk` (Minutes)\n"
            "• `/remind 19:30 call mom` (Specific time)\n"
            "• `/remind 31/03 09:00 exam` (Specific date)\n\n"
            "🔁 **Recurring**\n"
            "• `/remind daily 08:00 gym` (Every day)\n"
            "• `/remind weekly 10:00 Sunday Church` (Every week)"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")