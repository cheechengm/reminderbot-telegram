import time
from datetime import datetime
from database.database import reminders

def check_reminders(bot):
    while True:
        now = datetime.now()

        due = reminders.find({"remind_at": {"$lte": now}})

        for r in due:
            bot.send_message(
                chat_id=r["user_id"],
                text=f"⏰ Reminder: {r['message']}"
            )
            reminders.delete_one({"_id": r["_id"]})

        time.sleep(5)