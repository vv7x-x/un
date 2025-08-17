from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class TelegramWebhook(BaseModel):
	update_id: int
	message: Optional[dict] = None


@router.post("/telegram/webhook")
async def telegram_webhook(body: TelegramWebhook):
	# Stub: echo back
	return {"received": True, "update_id": body.update_id, "message": body.message}