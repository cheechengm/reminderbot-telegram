async def start(update, context):
    instructions = (
        "👋 **Hello! I'm your Smart Reminder Bot.**\n\n"
        "I'll make sure you never forget a task again. Here is how to use me:\n\n"
        "⏰ **Set a Reminder**\n"
        "• **Minutes:** `/remind 10 buy milk` (In 10 mins)\n"
        "• **Today:** `/remind 19:30 call mom` or `1930` (At 7:30 PM)\n"
        "• **Specific Date:** `/remind 31/03 10:00 meeting` (March 31st)\n\n"
        "🔁 **Recurring Reminders**\n"
        "• **Daily:** `/remind daily 08:00 Gym` (Triggers every day)\n"
        "• **Weekly:** `/remind weekly 10:00 Sunday Church` (Every week)\n\n"
        "📋 **Manage Reminders**\n"
        "• **Interactive List:** Type `/list` to see your reminders. You can delete them instantly using the **🗑️ Delete** buttons—no typing required!\n\n"
        "💡 **Pro Tips:**\n"
        "• All times are automatically handled in **Singapore Time (SGT)**.\n"
        "• If you set a time that has already passed today, I'll intelligently set it for tomorrow!"
    )
    
    await update.message.reply_text(instructions, parse_mode="Markdown")