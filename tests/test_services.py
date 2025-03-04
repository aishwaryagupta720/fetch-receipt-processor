from app.services.receipt_service import ReceiptService
from app.models.receipt import Receipt, Item

def test_calculate_points():
    receipt = Receipt(
        retailer="Target",
        purchaseDate="2022-01-01",
        purchaseTime="13:01",
        items=[
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"}
        ],
        total="13.51"
    )

    receipt_id = ReceiptService.process_receipt(receipt)
    points = ReceiptService.calculate_points(receipt_id)

    assert isinstance(points, int)
    assert points > 0  # Some points should be awarded

def test_nonexistent_receipt():
    points = ReceiptService.calculate_points("invalid-id")
    assert points is None
