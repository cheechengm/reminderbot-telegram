from bson.objectid import ObjectId
from database.database import reminders

async def handle_callback(update, context):
    query = update.callback_query
    data = query.data
    
    # Always answer the callback to remove the "loading" state on the button
    await query.answer()

    if data.startswith("del_"):
        reminder_id = data.split("_")[1]
        try:
            # Delete from DB
            result = reminders.delete_one({"_id": ObjectId(reminder_id)})
            
            if result.deleted_count > 0:
                # Update the message to show it was deleted
                await query.edit_message_text(text="✅ Reminder deleted.")
            else:
                await query.edit_message_text(text="⚠️ Reminder already removed or not found.")
        except Exception as e:
            print(f"Callback Error: {e}")
            await query.edit_message_text(text="❌ Error deleting reminder.")