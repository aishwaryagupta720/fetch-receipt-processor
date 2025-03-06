import math
from app.models.receipt import Receipt
from app.services.storage import StorageInterface
from datetime import datetime
from uuid import uuid4

class ReceiptService:
    """Handles business logic for receipts using dependency injection."""

    def __init__(self, storage: StorageInterface):
        self.storage = storage  

    def process_receipt(self, receipt: Receipt) -> str:
        """Stores the receipt and precomputes points."""

        receipt_id = str(uuid4())

        receipt_dict = receipt.model_dump()
        
        # Precompute points 
        points = self.calculate_points(receipt_dict)

        # Store points in memory 
        self.storage.save_points(receipt_id, points) 

        #Save receipt 
        self.storage.save_receipt(receipt_id,receipt_dict)

        return receipt_id

    def calculate_points(self, receipt: dict) -> int:
        """Computes points at receipt submission, so GET is instant."""
        points = 0

        # Rule 1: One point for every alphanumeric character in retailer name
        points += sum(c.isalnum() for c in receipt["retailer"])

        # Rule 2: 50 points if total is a round dollar amount
        total = float(receipt["total"])
        if total.is_integer():
            points += 50

        # Rule 3: 25 points if total is a multiple of 0.25
        if total % 0.25 == 0:
            points += 25

        # Rule 4: 5 points for every two items
        points += (len(receipt["items"]) // 2) * 5

        # Rule 5: If item description length (trimmed) is a multiple of 3
        for item in receipt["items"]:
            desc = item["shortDescription"].strip()
            if len(desc) % 3 == 0:
                points += math.ceil(float(item["price"]) * 0.2)

        # Rule 6: 6 points if the day in purchase date is odd
        purchase_date = datetime.strptime(receipt["purchaseDate"], "%Y-%m-%d").date()
        if purchase_date.day % 2 == 1:
            points += 6

        # Rule 7: 10 points if purchase time is between 2:01 PM and 3:59 PM
        purchase_time = datetime.strptime(receipt["purchaseTime"], "%H:%M").time()
        if (purchase_time.hour == 14 and purchase_time.minute >= 1) or (purchase_time.hour == 15):
            points += 10

        return points

    def get_points(self, receipt_id: str) -> int:
        """Instantly retrieves precomputed points from memory."""
        return self.storage.get_points(receipt_id)  
