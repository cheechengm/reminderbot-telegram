from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/{token}")
async def handler(request: Request):
    update = await request.json()
    await tg_app.update_queue.put(update)
    return {"ok": True}