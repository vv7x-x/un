# AI Provider Examples

```bash
# Ollama local
curl -sS http://127.0.0.1:8000/api/ai/complete -H 'content-type: application/json' -d '{
  "prompt": "Write a haiku about the moon.",
  "provider": "ollama",
  "model": "llama3.1"
}' | jq

# OpenAI
curl -sS http://127.0.0.1:8000/api/ai/complete -H 'content-type: application/json' -d '{
  "prompt": "List 3 creative startup ideas.",
  "provider": "openai",
  "model": "gpt-4o-mini"
}' | jq

# Gemini
curl -sS http://127.0.0.1:8000/api/ai/complete -H 'content-type: application/json' -d '{
  "prompt": "Explain quantum entanglement simply.",
  "provider": "gemini",
  "model": "gemini-1.5-flash"
}' | jq

# Anthropic
curl -sS http://127.0.0.1:8000/api/ai/complete -H 'content-type: application/json' -d '{
  "prompt": "Summarize the benefits of TDD.",
  "provider": "anthropic",
  "model": "claude-3-haiku-20240307"
}' | jq
```