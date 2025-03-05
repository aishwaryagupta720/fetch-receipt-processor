from app.services.receipt_service import ReceiptService
from app.services.memory_storage import InMemoryStorage

# Initialize the storage layer
storage = InMemoryStorage()

# Create a ReceiptService instance
receipt_service = ReceiptService(storage)

# Dependency provider function
def get_receipt_service() -> ReceiptService:
    return receipt_service
