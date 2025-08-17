from __future__ import annotations

from typing import Optional

import httpx
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from fastapi import APIRouter, HTTPException, Query

from backend.app.config import get_settings


router = APIRouter()


@router.get("/search")
async def search(q: str, max_results: int = 5):
	with DDGS() as ddgs:
		results = list(ddgs.text(q, max_results=max_results))
	return {"query": q, "results": results}


@router.get("/google")
async def google_search(q: str, max_results: int = 5):
	settings = get_settings()
	if not settings.google_api_key or not settings.google_cx:
		raise HTTPException(status_code=400, detail="Google API key or CX not configured")
	params = {
		"key": settings.google_api_key,
		"cx": settings.google_cx,
		"q": q,
		"num": max_results,
	}
	async with httpx.AsyncClient(timeout=30) as client:
		resp = await client.get("https://www.googleapis.com/customsearch/v1", params=params)
		resp.raise_for_status()
		data = resp.json()
		items = data.get("items", [])
		return {"query": q, "results": items}


@router.get("/fetch")
async def fetch(url: str):
	async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
		resp = await client.get(url)
		return {
			"url": url,
			"status": resp.status_code,
			"headers": dict(resp.headers),
			"text": resp.text[:20000],
		}


@router.get("/scrape")
async def scrape(url: str, selector: Optional[str] = Query(default=None)):
	async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
		resp = await client.get(url)
		if resp.status_code != 200:
			raise HTTPException(status_code=resp.status_code, detail="Fetch failed")
		soup = BeautifulSoup(resp.text, "html.parser")
		if selector:
			elements = [el.get_text(strip=True) for el in soup.select(selector)]
		else:
			elements = [p.get_text(strip=True) for p in soup.find_all("p")]
		return {"url": url, "count": len(elements), "items": elements[:200]}