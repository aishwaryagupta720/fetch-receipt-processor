from fastapi import APIRouter, HTTPException
from app.models.receipt import Receipt, ReceiptResponse, PointsResponse
from app.services.receipt_service import ReceiptService

router = APIRouter()

@router.post("/receipts/process", response_model=ReceiptResponse)
def process_receipt(receipt: Receipt):
    """Stores receipt and returns a unique receipt ID."""
    receipt_id = ReceiptService.process_receipt(receipt)
    return {"id": receipt_id}

@router.get("/receipts/{id}/points", response_model=PointsResponse)
def get_receipt_points(id: str):
    """Retrieves points for the given receipt ID."""
    points = ReceiptService.calculate_points(id)
    if points is None:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")
    return {"points": points}
