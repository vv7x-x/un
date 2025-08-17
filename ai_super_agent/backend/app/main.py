from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.router import router as api_router
from backend.app.config import get_settings
from backend.app.ws.manager import router as ws_router


@asynccontextmanager
def lifespan(app: FastAPI):
    settings = get_settings()

    # Load plugins if enabled
    if settings.plugin_autoload:
        try:
            from backend.app.plugins.loader import load_plugins

            load_plugins(app, settings)
        except Exception as exc:
            # Avoid failing app start if plugins fail to load
            print(f"[plugins] load failed: {exc}")

    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(api_router, prefix="/api")
    app.include_router(ws_router)

    @app.get("/health")
    def health():
        return {"status": "ok", "app": settings.app_name}

    return app


app = create_app()