from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

valid_receipt = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
        {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
        {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
    ],
    "total": "35.35"
}

def test_post_receipt():
    response = client.post("/receipts/process", json=valid_receipt)
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_receipt_points():
    post_response = client.post("/receipts/process", json=valid_receipt)
    receipt_id = post_response.json()["id"]

    get_response = client.get(f"/receipts/{receipt_id}/points")
    assert get_response.status_code == 200
    assert "points" in get_response.json()
    assert isinstance(get_response.json()["points"], int)

def test_invalid_receipt_id():
    invalid_receipt_id = 'abc'
    response = client.get(f"/receipts/{invalid_receipt_id}/points")
    assert response.status_code == 404
