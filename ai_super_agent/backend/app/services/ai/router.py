from __future__ import annotations

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.config import get_settings
from backend.app.services.ai.providers import ProviderName, get_provider


router = APIRouter()


class CompletionRequest(BaseModel):
	prompt: str
	provider: Optional[ProviderName] = None
	model: Optional[str] = None


@router.post("/complete")
async def complete(req: CompletionRequest):
	settings = get_settings()
	provider_name = req.provider or settings.default_ai_provider or "ollama"
	provider = get_provider(provider_name)  # type: ignore[arg-type]
	text = await provider.acomplete(prompt=req.prompt, model=req.model)
	return {"provider": provider_name, "model": req.model, "text": text}