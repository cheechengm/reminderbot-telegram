from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from database.database import reminders

async def list_reminders(update, context):
    user_id = update.message.chat_id
    # Find all reminders for this user, sorted by time
    user_reminders = list(reminders.find({"user_id": user_id}).sort("remind_at", 1))

    if not user_reminders:
        await update.message.reply_text("📭 You have no active reminders.")
        return

    # Use reply_text for the header
    await update.message.reply_text("📋 *Your Active Reminders:*", parse_mode="Markdown")

    for r in user_reminders:
        # 1. Convert UTC back to SGT for display (+8 hours)
        sgt_time = r['remind_at'] + timedelta(hours=8)
        
        # 2. Add the Day of the Week (e.g., Mon, 31 Mar | 19:30)
        time_str = sgt_time.strftime("%a, %d %b | %H:%M")
        
        # 3. Add a Repeat Icon if it's daily or weekly
        repeat_type = r.get("repeat")
        icon = "🔁 " if repeat_type else "⏰ "
        repeat_suffix = f" ({repeat_type.capitalize()})" if repeat_type else ""

        keyboard = [
            [
                InlineKeyboardButton("🗑️ Delete", callback_data=f"del_{r['_id']}"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # 4. Final formatted message
        await update.message.reply_text(
            f"{icon}*{time_str}*{repeat_suffix}\n"
            f"📝 {r['message']}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )