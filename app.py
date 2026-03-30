import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.start import start
from handlers.remind import remind
from handlers.list import list_reminders
from handlers.delete import delete_reminder
from services.reminder_service import check_reminders

TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_URL")

app = FastAPI()

# 1. Initialize global app object
tg_app = ApplicationBuilder().token(TOKEN).build()

@app.on_event("startup")
async def startup_event():
    # 🔥 This is the magic part: fire and forget
    asyncio.create_task(initialize_everything_bg())
    print("🚀 FastAPI startup function finished. Port opening now...")

async def initialize_everything_bg():
    try:
        print("🤖 Background: Registering handlers...")
        tg_app.add_handler(CommandHandler("start", start))
        tg_app.add_handler(CommandHandler("remind", remind))
        tg_app.add_handler(CommandHandler("list", list_reminders))
        tg_app.add_handler(CommandHandler("delete", delete_reminder))

        print("🤖 Background: Initializing Telegram...")
        await tg_app.initialize()
        
        print(f"🤖 Background: Setting webhook to {RENDER_URL}/{TOKEN}...")
        await tg_app.bot.set_webhook(f"{RENDER_URL}/{TOKEN}")
        
        # Store in app state so it's accessible elsewhere if needed
        app.state.tg_app = tg_app
        print("✅ Background: Bot is ready.")

        # ⏰ Start the reminder loop (Ensure this uses asyncio.sleep!)
        print("⏰ Background: Starting reminder loop...")
        await check_reminders(tg_app.bot)

    except Exception as e:
        print(f"❌ Background Error: {e}")

@app.post(f"/{TOKEN}")
async def webhook(request: Request):
    # Use the global tg_app to process updates
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def home():
    return {"status": "Bot is alive"}