import asyncio
from datetime import datetime
from database.database import reminders

async def check_reminders(bot):
    print("⏰ Reminder loop started...")
    while True:
        try:
            now = datetime.now()
            # Find reminders that are due
            due = reminders.find({"remind_at": {"$lte": now}})

            for r in due:
                # Use 'await' for the bot message
                await bot.send_message(
                    chat_id=r["user_id"],
                    text=f"⏰ Reminder: {r['message']}"
                )
                reminders.delete_one({"_id": r["_id"]})

        except Exception as e:
            print(f"❌ Error in reminder loop: {e}")

        # CRITICAL: This allows FastAPI to breathe and open the port
        await asyncio.sleep(5)