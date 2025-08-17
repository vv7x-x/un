from __future__ import annotations

from fastapi import FastAPI
from fastapi import APIRouter

from backend.app.plugins.plugin_base import BasePlugin, PluginMeta
from backend.app.services.ai.providers import get_provider


class HelloWorldPlugin(BasePlugin):
	def __init__(self) -> None:
		super().__init__(PluginMeta(name="hello_world", version="0.1.0", description="Demo plugin"))
		r = self.get_router()

		@r.get("/ping")
		def ping():
			return {"pong": True, "plugin": self.meta.name}

		@r.get("/ai")
		async def ai(prompt: str = "Say hello", provider: str = "ollama"):
			prov = get_provider(provider)  # type: ignore[arg-type]
			text = await prov.acomplete(prompt)
			return {"text": text}


def get_plugin(app: FastAPI, settings):
	return HelloWorldPlugin()