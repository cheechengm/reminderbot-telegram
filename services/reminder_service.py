import asyncio
from datetime import datetime, timedelta
from database.database import reminders

async def check_reminders(bot):
    print("⏰ Reminder loop started...")
    while True:
        try:
            # Use utcnow to match the UTC storage in your database
            now = datetime.utcnow()
            
            # Find reminders that are due
            due = reminders.find({"remind_at": {"$lte": now}})

            for r in due:
                try:
                    # 1. Send the message
                    await bot.send_message(
                        chat_id=r["user_id"],
                        text=f"⏰ **Reminder:** {r['message']}",
                        parse_mode="Markdown"
                    )

                    # 2. Handle Recurrence Logic
                    repeat_type = r.get("repeat")

                    if repeat_type == "daily":
                        # Reschedule for exactly 24 hours from the PREVIOUS set time
                        new_time = r["remind_at"] + timedelta(days=1)
                        reminders.update_one(
                            {"_id": r["_id"]}, 
                            {"$set": {"remind_at": new_time}}
                        )
                        print(f"🔁 Rescheduled daily task: {r['message']}")

                    elif repeat_type == "weekly":
                        # Reschedule for exactly 7 days later
                        new_time = r["remind_at"] + timedelta(weeks=1)
                        reminders.update_one(
                            {"_id": r["_id"]}, 
                            {"$set": {"remind_at": new_time}}
                        )
                        print(f"🔁 Rescheduled weekly task: {r['message']}")

                    else:
                        # If not recurring, delete it as usual
                        reminders.delete_one({"_id": r["_id"]})
                        print(f"✅ One-time task completed: {r['message']}")

                except Exception as send_error:
                    print(f"⚠️ Failed to send specific reminder: {send_error}")

        except Exception as e:
            print(f"❌ Error in reminder loop: {e}")

        # Wait 5 seconds before checking again
        await asyncio.sleep(5)