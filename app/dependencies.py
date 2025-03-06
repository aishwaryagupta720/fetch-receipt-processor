import logging
from app.services.receipt_service import ReceiptService
from app.services.memory_storage import InMemoryStorage

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO  
)

logger = logging.getLogger(__name__)

# Initialize the storage layer
storage = InMemoryStorage()
logger.info("InMemoryStorage initialized successfully.")

# Create a ReceiptService instance
receipt_service = ReceiptService(storage)
logger.info("ReceiptService instance created successfully.")

# Dependency provider function
def get_receipt_service() -> ReceiptService:
    logger.info("ReceiptService dependency injected.")
    return receipt_service
