from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import List, Optional

import psutil
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from backend.app.security import validate_shell_command


router = APIRouter()


class RunCommandRequest(BaseModel):
	cmd: str
	cwd: Optional[str] = None
	env: Optional[dict] = None
	timeout_seconds: Optional[int] = 60


@router.post("/run")
async def run_command(req: RunCommandRequest):
	args = validate_shell_command(req.cmd)
	cwd = req.cwd or str(Path.cwd())
	try:
		proc = await asyncio.create_subprocess_exec(
			*args,
			cwd=cwd,
			env={**os.environ, **(req.env or {})},
			stdout=asyncio.subprocess.PIPE,
			stderr=asyncio.subprocess.PIPE,
		)
		try:
			stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=req.timeout_seconds)
		except asyncio.TimeoutError:
			proc.kill()
			raise HTTPException(status_code=408, detail="Command timed out")
		return {
			"code": proc.returncode,
			"stdout": stdout.decode(errors="ignore"),
			"stderr": stderr.decode(errors="ignore"),
		}
	except FileNotFoundError:
		raise HTTPException(status_code=404, detail=f"Executable not found: {args[0]}")


@router.get("/files")
async def list_files(path: str = Query(default=".")):
	p = Path(path)
	if not p.exists():
		raise HTTPException(status_code=404, detail="Path not found")
	items = []
	for child in p.iterdir():
		items.append({
			"name": child.name,
			"is_dir": child.is_dir(),
			"size": child.stat().st_size,
		})
	return {"path": str(p.resolve()), "items": items}


@router.get("/processes")
async def processes():
	procs: List[dict] = []
	for p in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_info"]):
		info = p.info
		procs.append({
			"pid": info.get("pid"),
			"name": info.get("name"),
			"cpu": info.get("cpu_percent"),
			"mem": getattr(info.get("memory_info"), "rss", None),
		})
	return {"count": len(procs), "items": procs}