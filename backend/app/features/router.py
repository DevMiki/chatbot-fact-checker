from fastapi import APIRouter

from .chat.routes import router as chat_router
from .files.routes import router as files_router
from .health.routes import router as health_router

router = APIRouter()

router.include_router(health_router)
router.include_router(chat_router)
router.include_router(files_router)
