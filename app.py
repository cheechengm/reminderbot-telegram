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

bot = Bot(token=TOKEN)
tg_app = ApplicationBuilder().token(TOKEN).build()

# Register commands
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("remind", remind))
tg_app.add_handler(CommandHandler("list", list_reminders))
tg_app.add_handler(CommandHandler("delete", delete_reminder))

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Start reminders in background
    asyncio.create_task(check_reminders(bot))
    # Initialize bot and set webhook
    await tg_app.initialize()
    await bot.set_webhook(f"{RENDER_URL}/{TOKEN}")

@app.get("/")
async def home():
    return {"status": "Bot running!"}

@app.post(f"/{TOKEN}")
async def webhook(request: Request):
    update = await request.json()
    await tg_app.update_queue.put(update)
    return {"status": "ok"}