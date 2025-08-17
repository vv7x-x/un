# Web API Examples

```bash
# Search the web
curl -sS 'http://127.0.0.1:8000/api/web/search?q=fastapi websockets&max_results=3' | jq

# Fetch a URL
curl -sS 'http://127.0.0.1:8000/api/web/fetch?url=https://example.com' | jq

# Scrape paragraph texts
curl -sS 'http://127.0.0.1:8000/api/web/scrape?url=https://example.com' | jq

# Scrape with CSS selector
curl -sS 'http://127.0.0.1:8000/api/web/scrape?url=https://news.ycombinator.com&selector=.titleline a' | jq
```