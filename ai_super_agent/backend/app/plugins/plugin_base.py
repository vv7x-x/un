from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from fastapi import APIRouter


@dataclass
class PluginMeta:
    name: str
    version: str
    description: str = ""
    mount_path: Optional[str] = None  # default to /plugins/{name}


class BasePlugin:
    def __init__(self, meta: PluginMeta) -> None:
        self.meta = meta
        self.router = APIRouter()

    def get_router(self) -> APIRouter:
        return self.router