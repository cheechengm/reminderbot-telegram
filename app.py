import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.start import start
from handlers.remind import remind
from handlers.list import list_reminders
from handlers.delete import delete_reminder
from services.reminder_service import check_reminders

TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_URL")
PORT = int(os.getenv("PORT", 10000)) # Render provides this

app = FastAPI()

# 1. Initialize the Application object globally once
tg_app = ApplicationBuilder().token(TOKEN).build()

@app.on_event("startup")
async def startup_event():
    # Register handlers
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(CommandHandler("remind", remind))
    tg_app.add_handler(CommandHandler("list", list_reminders))
    tg_app.add_handler(CommandHandler("delete", delete_reminder))

    # Initialize the bot app (but don't start_polling)
    await tg_app.initialize()
    await tg_app.bot.set_webhook(f"{RENDER_URL}/{TOKEN}")
    
    # 2. Store in app state
    app.state.tg_app = tg_app

    # 3. Start background tasks WITHOUT blocking
    asyncio.create_task(run_reminder_loop())
    print("✅ Port should now open and server start.")

async def run_reminder_loop():
    print("⏰ Starting reminder loop...")
    # Ensure check_reminders is an async function with an internal 'while True' loop
    # and a 'await asyncio.sleep()' to prevent CPU hogging
    await check_reminders(tg_app.bot)

@app.post(f"/{TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def home():
    return {"status": "Bot is alive"}