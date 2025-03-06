import threading
from uuid import uuid4
from app.services.storage import StorageInterface

class InMemoryStorage(StorageInterface):
    """Thread-safe in-memory storage implementation."""

    def __init__(self):
        self.receipts_db = {}
        self.points_db = {} 
        self.lock = threading.Lock()

    def save_receipt(self, receipt_id,receipt: dict) -> str:
        """Save a receipt and return a unique receipt ID."""
        with self.lock:
            self.receipts_db[receipt_id] = receipt

    def get_receipt(self, receipt_id: str):
        """Retrieve a receipt by ID."""
        return self.receipts_db.get(receipt_id)
        
    def save_points(self, receipt_id: str, points: int):
        """Store points separately to avoid write locks on receipts."""
        with self.lock:
            self.points_db[receipt_id] = points  

    def get_points(self, receipt_id: str):
        """Instantly retrieve precomputed points."""
        return self.points_db.get(receipt_id, None)
