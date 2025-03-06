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
    items: List[Item] = Field(..., min_length=1, description="At least one item is required")
    total: str = Field(..., pattern=r"^\d+\.\d{2}$", description="Total must be a valid decimal format")


    @field_validator("purchaseDate", mode="before")
    @classmethod
    def validate_purchase_date(cls, value):
        """Validates `purchaseDate` format and ensures it is not null or empty."""
        if not value:
            raise ValueError("purchaseDate cannot be null or empty.")
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid purchaseDate format. Expected YYYY-MM-DD.")
        return value

    @field_validator("purchaseTime", mode="after")
    @classmethod
    def validate_purchase_time(cls, value: str, values: ValidationInfo):
        """Validates `purchaseTime` format and ensures it's not in the future."""
        if not value:
            raise ValueError("purchaseTime cannot be null or empty.")

        # Validate format
        try:
            purchase_time = datetime.strptime(value, "%H:%M").time()
        except ValueError:
            raise ValueError("Invalid purchaseTime format. Expected HH:MM (24-hour).")

        # Ensure purchaseTime is in the past
        purchase_date = values.data.get("purchaseDate")
        if purchase_date:
            try:
                purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d").date()
                purchase_datetime = datetime.combine(purchase_date, purchase_time)
                if purchase_datetime > datetime.now():
                    raise ValueError("Purchase cannot be in the future.")
            except ValueError:
                raise ValueError("Invalid purchaseDate format while validating purchaseTime.")

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
