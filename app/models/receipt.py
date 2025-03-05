from pydantic import BaseModel, Field,validator
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

    @validator("purchaseDate")
    def validate_purchase_date(cls, value):
        """Convert string to date object and validate."""
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d").date()
            return value  # Store as string (per OpenAPI spec)
        except ValueError:
            raise ValueError("Invalid purchaseDate format. Expected YYYY-MM-DD.")

    @validator("purchaseTime")
    def validate_purchase_time(cls, value):
        """Convert string to time object and validate."""
        try:
            time_obj = datetime.strptime(value, "%H:%M").time()
            return value  # Store as string (per OpenAPI spec)
        except ValueError:
            raise ValueError("Invalid purchaseTime format. Expected HH:MM (24-hour).")



class ReceiptResponse(BaseModel):
    """Defines the response when submitting a receipt."""
    id: str = Field(..., pattern=r"^\S+$", description="Receipt ID")

class PointsResponse(BaseModel):
    """Defines the response when retrieving points."""
    points: int
