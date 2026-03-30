# app.py
import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.start import start
from handlers.remind import remind
from handlers.list import list_reminders
from handlers.delete import delete_reminder
from services.reminder_service import check_reminders

TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_URL")  

# Initialize bot objects
bot = Bot(token=TOKEN)
tg_app = ApplicationBuilder().token(TOKEN).build()

# Register commands
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("remind", remind))
tg_app.add_handler(CommandHandler("list", list_reminders))
tg_app.add_handler(CommandHandler("delete", delete_reminder))

# Initialize FastAPI
app = FastAPI()

async def init_bot():
    """
    Initialize the Telegram bot and set webhook.
    This runs in background to prevent blocking FastAPI startup.
    """
    await tg_app.initialize()
    await bot.set_webhook(f"{RENDER_URL}/{TOKEN}")

@app.on_event("startup")
async def startup_event():
    # Start reminders service in background
    asyncio.create_task(check_reminders(bot))
    # Initialize Telegram bot in background
    asyncio.create_task(init_bot())

@app.get("/")
async def home():
    return {"status": "Bot running!"}

@app.post(f"/{TOKEN}")
async def webhook(request: Request):
    """
    Telegram webhook endpoint. Push updates into bot's update queue.
    """
    update = await request.json()
    await tg_app.update_queue.put(update)
    return {"status": "ok"}