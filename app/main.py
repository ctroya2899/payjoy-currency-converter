from fastapi import FastAPI

from app.routes import router

app = FastAPI(
    title="PayJoy Currency Conversion API",
    description="Converts USD amounts to local currencies using live exchange rates.",
    version="1.0.0",
)

app.include_router(router)