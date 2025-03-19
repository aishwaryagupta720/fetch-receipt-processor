import pytest
from pydantic import ValidationError
from app.models.receipt import Receipt, Item

def test_valid_item():
    """Test valid item creation."""
    item = Item(shortDescription="Mountain Dew 12PK", price="6.49")
    assert item.shortDescription == "Mountain Dew 12PK"
    assert item.price == "6.49"

@pytest.mark.parametrize("shortDescription, price, should_raise", [
    ("Valid Item", "10.00", False),  
    ("", "5.99", True),  # Empty description
    ("Item", "10", True),  # No decimal places
    ("Item", "-5.00", True),  # Negative price
    ("Item", "abc", True),  # Non-numeric price
])
def test_item_validation(shortDescription, price, should_raise):
    """Test different cases for item validation."""
    if should_raise:
        with pytest.raises(ValidationError):
            Item(shortDescription=shortDescription, price=price)
    else:
        item = Item(shortDescription=shortDescription, price=price)
        assert item.shortDescription == shortDescription
        assert item.price == price

@pytest.mark.parametrize("purchaseDate, should_raise", [
    ("2023-02-29", True),  # Invalid leap year
    ("2024-02-29", False),  # Valid leap year
    ("2022-13-01", True),  # Invalid month
    ("2022-01-32", True),  # Invalid day
    ("2027-01-22", True),  # future day
])
def test_purchase_date_validation(purchaseDate, should_raise):
    """Test purchase date validation."""
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": purchaseDate,
        "purchaseTime": "13:01",
        "items": [{"shortDescription": "Item A", "price": "10.00"}],
        "total": "10.00"
    }
    try:
        receipt = Receipt(**receipt_data)
        assert not should_raise, f"Expected validation error for {purchaseDate}, but none occurred."
        assert receipt.purchaseDate == purchaseDate, f"Expected {purchaseDate}, but got {receipt.purchaseDate}"
    except ValidationError:
        assert should_raise, f"Unexpected validation error for {purchaseDate}"

@pytest.mark.parametrize("total, items, should_raise", [
    ("10.00", [{"shortDescription": "Item A", "price": "10.00"}], False),
    ("5.00", [{"shortDescription": "Item A", "price": "2.50"}, {"shortDescription": "Item B", "price": "2.50"}], False),
    ("10.01", [{"shortDescription": "Item A", "price": "10.00"}], True),  # Mismatch
])
def test_total_validation(total, items, should_raise):
    """Ensure total matches the sum of items."""
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": items,
        "total": total
    }

    expected_total = f"{sum(float(item['price']) for item in items):.2f}"

    try:
        receipt = Receipt(**receipt_data)
        assert not should_raise, f"Expected validation error for total={total}, but none occurred."
        assert receipt.total == expected_total, f"Expected total={expected_total}, but got {receipt.total}"
    except ValidationError:
        assert should_raise, f"Unexpected validation error for total={total}"
