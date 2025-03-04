from uuid import uuid4
from datetime import datetime
from app.models.receipt import Receipt

class ReceiptService:
    """Service class for processing receipts and calculating points."""
    
    receipts_db = {}  # Temporary in-memory storage (Replace with DB later)

    @staticmethod
    def process_receipt(receipt: Receipt) -> str:
        """
        Stores the receipt and assigns a unique ID.
        """
        receipt_id = str(uuid4())
        ReceiptService.receipts_db[receipt_id] = receipt.dict()
        return receipt_id

    @staticmethod
    def calculate_points(receipt_id: str) -> int:
        """
        Fetches the receipt and calculates points based on business rules.
        """
        if receipt_id not in ReceiptService.receipts_db:
            return None  # Receipt not found

        receipt = ReceiptService.receipts_db[receipt_id]
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
                points += round(float(item["price"]) * 0.2)

        # Rule 6: 5 extra points if total is greater than 10.00
        if total > 10.00:
            points += 5

        # Rule 7: 6 points if the day in purchase date is odd
        purchase_day = int(receipt["purchaseDate"].split("-")[-1])
        if purchase_day % 2 == 1:
            points += 6

        # Rule 8: 10 points if purchase time is between 2:00 PM and 3:59 PM
        purchase_time = datetime.strptime(receipt["purchaseTime"], "%H:%M").time()
        if 14 <= purchase_time.hour < 16:
            points += 10

        return points
