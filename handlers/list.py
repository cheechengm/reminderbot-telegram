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

    await update.message.reply_text("📋 *Your Active Reminders:*", parse_mode="Markdown")

    for r in user_reminders:
        # Convert UTC back to SGT for display (+8 hours)
        sgt_time = r['remind_at'] + timedelta(hours=8)
        time_str = sgt_time.strftime("%d %b, %H:%M")
        
        # We store the MongoDB _id in the callback_data so we know which one to delete
        keyboard = [
            [
                InlineKeyboardButton("🗑️ Delete", callback_data=f"del_{r['_id']}"),
                # Optional: Add an edit button if you want to implement it later
                # InlineKeyboardButton("✏️ Edit", callback_data=f"edit_{r['_id']}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"⏰ *{time_str}*\n📝 {r['message']}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )