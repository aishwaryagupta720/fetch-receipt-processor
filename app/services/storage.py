from abc import ABC, abstractmethod
from typing import Optional

class StorageInterface(ABC):
    """Abstract class for receipt storage."""

    @abstractmethod
    def save_receipt(self, receipt: dict) -> str:
        """Save a receipt and return its ID."""
        pass

    @abstractmethod
    def get_receipt(self, receipt_id: str) -> Optional[dict]:
        """Retrieve a receipt by ID."""
        pass
    
    @abstractmethod
    def save_points(self, receipt_id: str, points: int) -> None:
        """Save receipt points by ID."""
        pass

    @abstractmethod
    def get_points(self, receipt_id: str)-> Optional[int]:
        """Get receipt points by ID."""
        pass