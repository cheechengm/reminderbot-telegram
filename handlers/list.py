from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from database.database import reminders

async def list_reminders(update, context):
    user_id = update.message.chat_id
    user_reminders = list(reminders.find({"user_id": user_id}).sort("remind_at", 1))

    if not user_reminders:
        await update.message.reply_text("📭 **You have no active reminders.**", parse_mode="Markdown")
        return

    # We send the "Header" once. 
    # TIP: You could also delete the previous header to keep the chat clean!
    await update.message.reply_text("📋 *Active Reminders:*", parse_mode="Markdown")

    for r in user_reminders:
        # 1. Standardize SGT conversion
        sgt_time = r['remind_at'] + timedelta(hours=8)
        
        # 2. Format: "Mon, 31 Mar | 19:30"
        time_str = sgt_time.strftime("%a, %d %b | %H:%M")
        
        # 3. Handle Icons and Repeat Labels
        repeat_type = r.get("repeat")
        icon = "🔁" if repeat_type else "⏰"
        repeat_label = f" [{repeat_type.upper()}]" if repeat_type else ""

        # 4. COMPACT KEYBOARD (Better for 'Card' feel)
        # We put the icon inside the button text to save space
        keyboard = [[InlineKeyboardButton(f"🗑️ Delete Reminder", callback_data=f"del_{r['_id']}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # 5. CLEANER MESSAGE BODY
        # We use a code block for the time to make it stand out visually
        formatted_message = (
            f"{icon} `{time_str}`{repeat_label}\n"
            f"└─ **{r['message']}**"
        )

        await update.message.reply_text(
            formatted_message,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )