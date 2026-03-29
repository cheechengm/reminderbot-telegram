from flask import request
from telegram import Update

def webhook_handler(tg_app, bot):
    def handler():
        update = Update.de_json(request.get_json(), bot)
        tg_app.update_queue.put(update)
        return "ok"
    return handler