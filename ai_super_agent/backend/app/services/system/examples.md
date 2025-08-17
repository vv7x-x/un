# System API Examples

```bash
# Run allowed command (sandboxed)
curl -sS http://127.0.0.1:8000/api/system/run -H 'content-type: application/json' -d '{
  "cmd": "echo hello",
  "timeout_seconds": 3
}' | jq

# List files in backend
curl -sS 'http://127.0.0.1:8000/api/system/files?path=backend' | jq

# Processes snapshot
curl -sS http://127.0.0.1:8000/api/system/processes | jq
```