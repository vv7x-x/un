from __future__ import annotations

import shlex
from typing import Iterable, List, Optional

from fastapi import Depends, Header, HTTPException, status

from backend.app.config import get_settings


def require_admin(x_admin_key: Optional[str] = Header(default=None)) -> None:
	settings = get_settings()
	if settings.admin_api_key and x_admin_key != settings.admin_api_key:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin key")


DEFAULT_ALLOWED_COMMANDS: List[str] = [
	"ls", "dir", "cat", "type", "pwd", "echo", "whoami", "python", "python3",
	"pip", "pip3", "node", "npm", "npx", "git", "ffmpeg",
]


def is_command_allowed(command: List[str]) -> bool:
	settings = get_settings()
	if not settings.enable_sandbox:
		return True
	if not command:
		return False
	base = command[0]
	return base in DEFAULT_ALLOWED_COMMANDS


def validate_shell_command(cmdline: str) -> List[str]:
	parts = shlex.split(cmdline)
	if not is_command_allowed(parts):
		raise HTTPException(status_code=400, detail=f"Command not allowed in sandbox: {parts[0] if parts else ''}")
	return parts