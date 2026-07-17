from fastapi import FastAPI

from app.api.v1.contact import router as contact_router
from app.api.v1.health import router as health_router
from app.api.v1.metrics import router as metrics_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="Feedback Service")

app.include_router(contact_router)
app.include_router(health_router)
app.include_router(metrics_router)