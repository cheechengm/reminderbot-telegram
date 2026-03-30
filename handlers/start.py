async def start(update, context):
    instructions = (
        "👋 **Hello! I'm your Reminder Bot.**\n\n"
        "I can help you stay on track. Here is how to use me:\n\n"
        "⏰ **Set a Reminder**\n"
        "• By minutes: `/remind 10 buy milk` (Reminds you in 10 mins)\n"
        "• By time: `/remind 19:30 call mom` (Reminds you at 7:30 PM)\n\n"
        "📋 **Manage Reminders**\n"
        "• View all: `/list` (Shows your active reminders with IDs)\n"
        "• Remove one: `/delete 1` (Deletes reminder #1 from your list)\n\n"
        "💡 *Tip: If you set a time that has already passed today, I'll automatically set it for tomorrow!*"
    )
    
    await update.message.reply_text(instructions, parse_mode="Markdown")