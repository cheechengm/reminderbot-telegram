# routes/webhook.py
from flask import request
import asyncio

def webhook_handler(tg_app, bot):
    def handler():
        update = request.get_json()
        print("Received update:", update)  # DEBUG

        # Put the update into the async queue properly
        asyncio.create_task(tg_app.update_queue.put(update))

        return "OK"
    return handler