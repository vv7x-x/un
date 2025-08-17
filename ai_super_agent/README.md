# AI Super Agent

A cross-platform, modular AI agent with multi-provider intelligence, system control, web integrations, plugins, and multiple UIs (PyQt6, Flet, Flutter).

## Structure

```
ai_super_agent/
  backend/
    app/
      api/
        router.py
      config.py
      main.py
      ws/
        manager.py
      security.py
      plugins/
        plugin_base.py
        loader.py
      services/
        __init__.py
        ai/
          __init__.py
          providers.py
          router.py
        system/
          router.py
        web/
          __init__.py
          router.py
        comm/
          __init__.py
          router.py
    requirements.txt
    run.sh
  frontend/
    pyqt6_app/
    flet_app/
    flutter_app/
  .env.example
```

## Backend

- Python FastAPI with plugin loader and WebSocket manager
- AI providers: OpenAI, Gemini, Anthropic, Ollama
- Modules: AI (/api/ai), System (/api/system), Web (/api/web), Comm (/api/comm)

### Setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
# Edit ../.env to add API keys as needed
bash run.sh
```

Open: http://localhost:8000/docs

## UIs

Three UI variants will be provided:
- PyQt6 desktop
- Flet desktop/web
- Flutter desktop/web/mobile

Each UI will communicate with the FastAPI backend via REST/WebSocket.

## Plugins

Place plugins under `backend/app/plugins/<plugin_name>/plugin.py` exposing a `get_plugin(app, settings)` function returning an instance of a class derived from `BasePlugin` with a `router`.

Example:

```python
from backend.app.plugins.plugin_base import BasePlugin, PluginMeta
from fastapi import APIRouter

class MyPlugin(BasePlugin):
    def __init__(self):
        super().__init__(PluginMeta(name="hello", version="0.1.0"))
        r = self.get_router()
        @r.get("/ping")
        def ping():
            return {"pong": True}

def get_plugin(app, settings):
    return MyPlugin()
```

It will be mounted at `/plugins/hello`.

## Notes

- Sandbox restricts shell commands by default. Disable via `.env` if needed.
- For local LLMs, run Ollama and pull a model: `ollama pull llama3.1`.