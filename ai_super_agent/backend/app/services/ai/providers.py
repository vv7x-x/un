from __future__ import annotations

from typing import Literal, Optional

import httpx

from backend.app.config import get_settings


ProviderName = Literal["openai", "gemini", "anthropic", "ollama"]


class AIProvider:
	async def acomplete(self, prompt: str, model: Optional[str] = None) -> str:
		raise NotImplementedError


class OpenAIProvider(AIProvider):
	def __init__(self) -> None:
		self.api_key = get_settings().openai_api_key

	async def acomplete(self, prompt: str, model: Optional[str] = None) -> str:
		from openai import AsyncOpenAI

		client = AsyncOpenAI(api_key=self.api_key)
		model_name = model or "gpt-4o-mini"
		resp = await client.chat.completions.create(
			model=model_name,
			messages=[{"role": "user", "content": prompt}],
		)
		return resp.choices[0].message.content or ""


class GeminiProvider(AIProvider):
	def __init__(self) -> None:
		self.api_key = get_settings().google_api_key

	async def acomplete(self, prompt: str, model: Optional[str] = None) -> str:
		import google.generativeai as genai

		genai.configure(api_key=self.api_key)
		model_name = model or "gemini-1.5-flash"
		model_obj = genai.GenerativeModel(model_name)
		resp = await model_obj.generate_content_async(prompt)
		return getattr(resp, "text", "") or ""


class AnthropicProvider(AIProvider):
	def __init__(self) -> None:
		self.api_key = get_settings().anthropic_api_key

	async def acomplete(self, prompt: str, model: Optional[str] = None) -> str:
		from anthropic import AsyncAnthropic

		client = AsyncAnthropic(api_key=self.api_key)
		model_name = model or "claude-3-haiku-20240307"
		resp = await client.messages.create(
			model=model_name,
			max_tokens=512,
			messages=[{"role": "user", "content": prompt}],
		)
		# Anthropics returns content blocks
		blocks = getattr(resp, "content", [])
		for block in blocks:
			if getattr(block, "type", "") == "text":
				return getattr(block, "text", "")
		return ""


class OllamaProvider(AIProvider):
	def __init__(self) -> None:
		self.host = get_settings().ollama_host.rstrip("/")

	async def acomplete(self, prompt: str, model: Optional[str] = None) -> str:
		model_name = model or "llama3.1"
		async with httpx.AsyncClient(timeout=60) as client:
			resp = await client.post(f"{self.host}/api/generate", json={"model": model_name, "prompt": prompt, "stream": False})
			resp.raise_for_status()
			data = resp.json()
			return data.get("response", "")


def get_provider(name: ProviderName) -> AIProvider:
	if name == "openai":
		return OpenAIProvider()
	if name == "gemini":
		return GeminiProvider()
	if name == "anthropic":
		return AnthropicProvider()
	if name == "ollama":
		return OllamaProvider()
	raise ValueError(f"Unknown provider: {name}")