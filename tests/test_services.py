import pytest
from app.services.receipt_service import ReceiptService
from app.services.memory_storage import InMemoryStorage
from app.models.receipt import Receipt

@pytest.fixture
def receipt_service():
    """Provides a fresh ReceiptService instance with an in-memory store."""
    return ReceiptService(storage=InMemoryStorage())

def test_process_receipt(receipt_service):
    """Test storing a receipt and generating an ID."""
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-01-01",
        purchaseTime="13:01",
        items=[{"shortDescription": "Item A", "price": "10.00"}],
        total="10.00"
    )
    receipt_id = receipt_service.process_receipt(receipt)
    assert isinstance(receipt_id, str)
    assert len(receipt_id) > 0

def test_calculate_points(receipt_service):
    """Test point calculation logic."""
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-01-01",
        purchaseTime="14:30",  # Should trigger time bonus
        items=[
            {"shortDescription": "Item A", "price": "10.00"},
            {"shortDescription": "Item B", "price": "5.00"}
        ],
        total="15.00"
    )
    points = receipt_service.calculate_points(receipt.model_dump())
    assert isinstance(points, int)
    assert points > 0

def test_get_points(receipt_service):
    """Ensure points retrieval works correctly."""
    receipt = Receipt(
        retailer="Test Store",
        purchaseDate="2023-01-01",
        purchaseTime="13:01",
        items=[{"shortDescription": "Item A", "price": "5.00"}],
        total="5.00"
    )
    receipt_id = receipt_service.process_receipt(receipt)
    points = receipt_service.get_points(receipt_id)
    assert isinstance(points, int)
    assert points > 0
