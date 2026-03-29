import os
import threading
from flask import Flask

from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.start import start
from handlers.remind import remind
from handlers.list import list_reminders
from handlers.delete import delete_reminder

from services.reminder_service import check_reminders
from routes.webhook import webhook_handler

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_URL")

bot = Bot(token=TOKEN)
tg_app = ApplicationBuilder().token(TOKEN).build()

# Register commands
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("remind", remind))
tg_app.add_handler(CommandHandler("list", list_reminders))
tg_app.add_handler(CommandHandler("delete", delete_reminder))

# Routes
@app.route("/")
def home():
    return "Bot running!"

app.add_url_rule(
    f"/{TOKEN}",
    view_func=webhook_handler(tg_app, bot),
    methods=["POST"]
)

if __name__ == "__main__":
    # Start background reminder checker
    threading.Thread(target=check_reminders, args=(bot,), daemon=True).start()

    # Initialize Telegram bot
    tg_app.initialize()

    # Set webhook to public Render URL
    bot.set_webhook(f"{RENDER_URL}/{TOKEN}")

    # Use Render-assigned port
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)