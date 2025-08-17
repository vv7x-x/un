from __future__ import annotations

import asyncio
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from backend.app.services.ai.providers import get_provider
from backend.app.ws.manager import ws_manager


class TaskScheduler:
	def __init__(self) -> None:
		self.scheduler = AsyncIOScheduler()

	def start(self) -> None:
		if not self.scheduler.running:
			self.scheduler.start()

	def stop(self) -> None:
		if self.scheduler.running:
			self.scheduler.shutdown()

	def schedule_ai_completion(self, when_cron: str, prompt: str, provider: str = "ollama", model: Optional[str] = None) -> None:
		def job():
			asyncio.create_task(self._run_job(prompt, provider, model))

		# Use cron trigger expression like "*/5 * * * *" every 5 minutes
		self.scheduler.add_job(job, trigger="cron", **self._parse_cron(when_cron))

	async def _run_job(self, prompt: str, provider: str, model: Optional[str]) -> None:
		try:
			prov = get_provider(provider)  # type: ignore[arg-type]
			text = await prov.acomplete(prompt=prompt, model=model)
			await ws_manager.broadcast(f"[scheduled][{provider}] {text[:200]}")
		except Exception as exc:
			await ws_manager.broadcast(f"[scheduled][error] {exc}")

	def _parse_cron(self, expr: str):
		# very basic: "m h dom mon dow" -> dict
		parts = [p.strip() for p in expr.split()]
		if len(parts) != 5:
			raise ValueError("Cron expression must have 5 fields")
		return {"minute": parts[0], "hour": parts[1], "day": parts[2], "month": parts[3], "day_of_week": parts[4]}


task_scheduler = TaskScheduler()