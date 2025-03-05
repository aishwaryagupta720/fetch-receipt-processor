from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Receipt Processor API",
    description="API for processing receipts and calculating points",
    version="1.0.0"
)

app.include_router(router)
