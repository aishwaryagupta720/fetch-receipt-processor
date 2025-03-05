from pydantic import BaseModel, Field,validator,field_validator,ValidationInfo
from typing import List
from datetime import datetime

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
        
    @field_validator("purchaseTime", mode="after")
    @classmethod
    def validate_purchase_time(cls, value: str, values: ValidationInfo):
        """Ensure `purchaseTime` is in the past, considering `purchaseDate`."""
        print(f"values received: {values}")  # Debugging

        # Get validated purchaseDate
        purchase_date = datetime.strptime(values.data.get("purchaseDate"), "%Y-%m-%d").date()
        purchase_time = datetime.strptime(value, "%H:%M").time()

        # Get current time
        now = datetime.now()
        purchase_datetime = datetime.combine(purchase_date, purchase_time)

        if purchase_datetime > now:
            raise ValueError("Purchase cannot be in the future.")

        return value
    
    @field_validator("total", mode="after")
    @classmethod
    def validate_total(cls, total: str, values: ValidationInfo):
        """Ensure `total` matches sum of `items.price` values."""
        items = values.data.get("items")  
        
        if not items:
            raise ValueError("Items list must be provided before validating total.")

        total_price = sum(float(item.price) for item in items)  
        total_value = float(total)

        if round(total_price, 2) != round(total_value, 2):
            raise ValueError(f"Total ({total}) does not match sum of item prices ({total_price}).")

        return total 



class ReceiptResponse(BaseModel):
    """Defines the response when submitting a receipt."""
    id: str = Field(..., pattern=r"^\S+$", description="Receipt ID")

class PointsResponse(BaseModel):
    """Defines the response when retrieving points."""
    points: int
