from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.scheduler.runner import task_scheduler


router = APIRouter()


class CronJobRequest(BaseModel):
	cron: str
	prompt: str
	provider: str = "ollama"
	model: str | None = None


@router.post("/start")
async def start_scheduler():
	task_scheduler.start()
	return {"started": True}


@router.post("/jobs/ai")
async def add_ai_job(req: CronJobRequest):
	try:
		task_scheduler.schedule_ai_completion(when_cron=req.cron, prompt=req.prompt, provider=req.provider, model=req.model)
		return {"scheduled": True}
	except Exception as exc:
		raise HTTPException(status_code=400, detail=str(exc))