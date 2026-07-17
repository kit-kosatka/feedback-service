import json
import time
from pathlib import Path

from fastapi import HTTPException, Request

from app.core.config import get_settings

settings = get_settings()

STORAGE_FILE = Path("logs/rate_limit.json")


def _load_storage() -> dict[str, list[float]]:
    if not STORAGE_FILE.exists():
        return {}
    with open(STORAGE_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save_storage(data: dict[str, list[float]]) -> None:
    STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


async def check_rate_limit(request: Request) -> None:
    client_ip = request.client.host
    now = time.time()
    window_start = now - settings.rate_limit_window_seconds

    storage = _load_storage()
    timestamps = [t for t in storage.get(client_ip, []) if t > window_start]

    if len(timestamps) >= settings.rate_limit_requests:
        raise HTTPException(
            status_code=429, detail="Слишком много запросов, попробуйте позже"
        )

    timestamps.append(now)
    storage[client_ip] = timestamps
    _save_storage(storage)
