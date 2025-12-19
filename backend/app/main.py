import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from .features.router import router as api_router
from .shared.config import settings
from .features.chat.correlation import SystemFileManager
from .features.chat.storage import ensure_storage_dirs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    ensure_storage_dirs()
    SystemFileManager(base_dir=settings.system_files_dir)
    logger.info("Startup complete: dirs ensured, system files ready.")
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(api_router, prefix="/api")
