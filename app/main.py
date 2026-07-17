import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.contact import router as contact_router
from app.api.v1.health import router as health_router
from app.api.v1.metrics import router as metrics_router
from app.core.config import get_settings
from app.core.exceptions import global_exception_handler
from app.core.logging import setup_logging

setup_logging()
settings = get_settings()
logger = logging.getLogger(__name__)

app = FastAPI(title="Feedback Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start) * 1000, 2)

    logger.info(
        "%s %s -> %s (%sms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    return response


app.include_router(contact_router)
app.include_router(health_router)
app.include_router(metrics_router)

app.add_exception_handler(Exception, global_exception_handler)
