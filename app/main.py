from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.routes import router
import logging
import json

app = FastAPI(
    title="Receipt Processor API",
    description="API for processing receipts and calculating points",
    version="1.0.0"
)

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Global Exception Handler for Validation Errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for validation errors.
    Logs the error details to the console.
    """

    error_details = json.dumps([str(error) for error in exc.errors()], indent=4)
    logger.error(f"Validation Error: {error_details}")

    return JSONResponse(
        status_code=400,
        content={"message": "The receipt is invalid."}
    )


# Include API Routes
app.include_router(router)
