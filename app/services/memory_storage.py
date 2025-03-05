import threading
from uuid import uuid4
from app.services.storage import StorageInterface

class InMemoryStorage(StorageInterface):
    """Thread-safe in-memory storage implementation."""

    def __init__(self):
        self.receipts_db = {}
        self.lock = threading.Lock()

    def save_receipt(self, receipt: dict) -> str:
        """Save a receipt and return a unique receipt ID."""
        receipt_id = str(uuid4())
        with self.lock:
            self.receipts_db[receipt_id] = receipt
        return receipt_id

    def get_receipt(self, receipt_id: str):
        """Retrieve a receipt by ID."""
        with self.lock:
            return self.receipts_db.get(receipt_id)
