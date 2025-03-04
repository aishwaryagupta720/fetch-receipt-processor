import pytest
from pydantic import ValidationError
from app.models.receipt import Receipt, Item

def test_valid_item():
    item = Item(shortDescription="Mountain Dew 12PK", price="6.49")
    assert item.shortDescription == "Mountain Dew 12PK"
    assert item.price == "6.49"

def test_invalid_item_price():
    with pytest.raises(ValidationError):
        Item(shortDescription="Mountain Dew 12PK", price="6.4") # Should fail (only 1 decimal)
        Item(shortDescription="Mountain Dew 12PK", price="6.489")  # Should fail (more than 2 decimal)

@pytest.mark.parametrize("items, should_raise_error", [
    ([{"shortDescription": "Item A", "price": "10.00"}], False),  # Valid single item
    ([{"shortDescription": "Item B", "price": "5.50"}, {"shortDescription": "Item C", "price": "3.99"}], False),  # Multiple items valid
    ([], True),  # Empty item list (invalid)
    ([{"shortDescription": "", "price": "10.00"}], True),  # Empty description (invalid)
    ([{"shortDescription": "Item A", "price": "10"}], True),  # Invalid price format (no decimals)
])
def test_items_validation(items, should_raise_error):
    """Test item array validation ensuring at least one valid item."""
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": items,
        "total": "10.00"
    }

    if should_raise_error:
        with pytest.raises(ValidationError):
            Receipt(**receipt_data)
    else:
        receipt = Receipt(**receipt_data)
        assert receipt.items == items

@pytest.mark.parametrize("total, should_raise_error", [
    ("10.00", False),  # Valid total
    ("9999999.99", False),  # Large valid total
    ("0.01", False),  # Smallest possible valid total
    ("10", True),  # Missing decimal places
    ("-5.00", True),  # Negative total (invalid)
    ("ABC", True),  # Non-numeric input
])
def test_total_validation(total, should_raise_error):
    """Test total price validation ensuring correct format and positive values."""
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"shortDescription": "Item A", "price": "10.00"}],
        "total": total
    }

    if should_raise_error:
        with pytest.raises(ValidationError):
            Receipt(**receipt_data)
    else:
        receipt = Receipt(**receipt_data)
        assert receipt.total == total


@pytest.mark.parametrize("retailer, should_raise_error", [
    ("Target", False),  # Valid retailer
    ("M&M Corner Market", False),  # Valid with special characters
    ("Shop-24&Go", False),  # Valid with allowed symbols
    ("12345", False),  # Retailer with numbers is valid
    ("", True),  # Empty retailer (invalid)
    ("Super@Store!", True),  # Contains invalid characters (@, !)
])
def test_retailer_validation(retailer, should_raise_error):
    """Test retailer name validation based on allowed characters."""
    receipt_data = {
        "retailer": retailer,
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"shortDescription": "Item A", "price": "10.00"}],
        "total": "10.00"
    }

    if should_raise_error:
        with pytest.raises(ValidationError):
            Receipt(**receipt_data)
    else:
        receipt = Receipt(**receipt_data)
        assert receipt.retailer == retailer

@pytest.mark.parametrize("purchase_date, should_raise_error", [
    ("2022-01-01", False),  # Valid date
    ("1999-12-31", False),  # Valid historical date
    ("2024-02-29", False),  # Leap year (valid)
    ("2023-02-29", True),  # Non-leap year (invalid)
    ("2023-04-31", True),  # April has 30 days (invalid)
    ("2022-13-01", True),  # Invalid month (13)
    ("2022-00-10", True),  # Invalid month (00)
    ("2022-01-00", True),  # Invalid day (00)
    ("2022-01-32", True),  # Invalid day (out of range)
    ("22-01-01", True),  # Incorrect format (YY instead of YYYY)
    ("01-01-2022", True),  # Incorrect format (MM-DD-YYYY)
    ("abc-def-ghi", True),  # Non-numeric input
])
def test_purchase_date_validation(purchase_date, should_raise_error):
    """Test that purchaseDate must be a valid YYYY-MM-DD format and within range."""
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": purchase_date,
        "purchaseTime": "13:01",
        "items": [{"shortDescription": "Item A", "price": "10.00"}],
        "total": "10.00"
    }

    if should_raise_error:
        with pytest.raises(ValidationError):
            Receipt(**receipt_data)
    else:
        receipt = Receipt(**receipt_data)
        assert receipt.purchaseDate == purchase_date  # Ensure date is stored correctly


@pytest.mark.parametrize("purchase_time, should_raise_error", [
    ("00:00", False),  # Midnight (valid)
    ("09:30", False),  # Morning (valid)
    ("13:59", False),  # 1:59 PM (valid)
    ("23:59", False),  # Last minute of the day (valid)
    ("24:00", True),  # Invalid hour (out of range)
    ("12:60", True),  # Invalid minutes (out of range)
    ("7:30", True),  # Missing leading zero (invalid format)
    ("99:99", True),  # Completely invalid time
    ("abc:ef", True),  # Non-numeric input
])
def test_purchase_time_validation(purchase_time, should_raise_error):
    """Test that purchaseTime must be a valid HH:MM format in 24-hour time."""
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": purchase_time,
        "items": [{"shortDescription": "Item A", "price": "10.00"}],
        "total": "10.00"
    }

    if should_raise_error:
        with pytest.raises(ValidationError):
            Receipt(**receipt_data)
    else:
        receipt = Receipt(**receipt_data)
        assert receipt.purchaseTime == purchase_time  # Ensure time is stored correctly

