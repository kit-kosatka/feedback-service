from fastapi import FastAPI

app = FastAPI(title="Feedback Service")


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok"}