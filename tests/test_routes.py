from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

valid_receipt = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
    ],
    "total": "18.74"
}

def test_post_receipt():
    """Test receipt submission endpoint."""
    response = client.post("/receipts/process", json=valid_receipt)
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_receipt_points():
    """Test points retrieval endpoint."""
    post_response = client.post("/receipts/process", json=valid_receipt)
    receipt_id = post_response.json()["id"]

    get_response = client.get(f"/receipts/{receipt_id}/points")
    assert get_response.status_code == 200
    assert "points" in get_response.json()
    assert isinstance(get_response.json()["points"], int)

def test_invalid_receipt():
    """Test invalid receipt submission."""
    invalid_receipt = valid_receipt.copy()
    invalid_receipt["total"] = "INVALID"
    response = client.post("/receipts/process", json=invalid_receipt)
    assert response.status_code == 400
    assert response.json() == {"message": "The receipt is invalid."}

def test_invalid_receipt_id():
    """Test retrieval with non-existent receipt ID."""
    response = client.get("/receipts/invalid-id/points")
    assert response.status_code == 404
    assert response.json() == {"detail": "No receipt found for that ID."}
