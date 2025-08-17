from fastapi import APIRouter

router = APIRouter()

# Import existing routers. Optional imports allow progressive build-out.
try:
    from backend.app.services.ai.router import router as ai_router

    router.include_router(ai_router, prefix="/ai", tags=["ai"])
except Exception:
    pass

try:
    from backend.app.services.system.router import router as system_router

    router.include_router(system_router, prefix="/system", tags=["system"])
except Exception:
    pass

try:
    from backend.app.services.web.router import router as web_router

    router.include_router(web_router, prefix="/web", tags=["web"])
except Exception:
    pass

try:
    from backend.app.services.comm.router import router as comm_router

    router.include_router(comm_router, prefix="/comm", tags=["comm"])
except Exception:
    pass

try:
    from backend.app.services.hardware.router import router as hw_router

    router.include_router(hw_router, prefix="/hardware", tags=["hardware"])
except Exception:
    pass

try:
    from backend.app.services.scheduler.router import router as scheduler_router

    router.include_router(scheduler_router, prefix="/scheduler", tags=["scheduler"])
except Exception:
    pass

# Future modules (security, assistant) will be added similarly.