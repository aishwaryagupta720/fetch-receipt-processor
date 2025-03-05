from pydantic import BaseModel, Field
from typing import List

class Item(BaseModel):
    """Defines an item on the receipt."""
    shortDescription: str = Field(..., pattern=r"^[\w\s\-]+$", description="Item description")
    price: str = Field(..., pattern=r"^\d+\.\d{2}$", description="Price as a string with 2 decimal places")

class Receipt(BaseModel):
    """Defines a receipt schema for validation."""
    retailer: str = Field(..., pattern=r"^[\w\s\-\&]+$", description="Retailer name")
    purchaseDate: str = Field(..., description="YYYY-MM-DD format")
    purchaseTime: str = Field(..., description="24-hour HH:MM format")
    items: List[Item] = Field(..., min_items=1, description="At least one item is required")
    total: str = Field(..., pattern=r"^\d+\.\d{2}$", description="Total must be a valid decimal format")

class ReceiptResponse(BaseModel):
    """Defines the response when submitting a receipt."""
    id: str = Field(..., pattern=r"^\S+$", description="Receipt ID")

class PointsResponse(BaseModel):
    """Defines the response when retrieving points."""
    points: int
