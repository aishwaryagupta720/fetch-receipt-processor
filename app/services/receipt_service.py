import math
from app.models.receipt import Receipt
from app.services.storage import StorageInterface
from datetime import datetime
from uuid import uuid4
import logging

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO  # Change to DEBUG for more insights
)

logger = logging.getLogger(__name__) 

class ReceiptService:
    """Handles business logic for receipts using dependency injection."""

    def __init__(self, storage: StorageInterface):
        self.storage = storage  

    def process_receipt(self, receipt: Receipt) -> str:
        """Stores the receipt and precomputes points."""
        receipt_id = str(uuid4())

        receipt_dict = receipt.model_dump()
        logger.info(f"Processing receipt : (ID: {receipt_id})")

        try:
            # Precompute points 
            points = self.calculate_points(receipt_dict)
            logger.info(f"Points calculated successfully for receipt ID: {receipt_id}, Total Points: {points}")

            # Store points in memory 
            self.storage.save_points(receipt_id, points) 
            logger.info(f"Points stored successfully: {receipt_id}")

            # Save receipt 
            self.storage.save_receipt(receipt_id, receipt_dict)
            logger.info(f"Receipt stored successfully: {receipt_id}")

            return receipt_id
        except Exception as e:
            logger.error(f"Error processing receipt ID: {receipt_id} - {str(e)}")
            raise

    def calculate_points(self, receipt: dict) -> int:
        """Computes points at receipt submission, so GET is instant."""

        points = 0
        total = float(receipt["total"])

        # Rule 1: One point for every alphanumeric character in retailer name
        retailer_points = sum(c.isalnum() for c in receipt["retailer"])
        points += retailer_points
        # logger.debug(f"Retailer name points: {retailer_points}")

        # Rule 2: 50 points if total is a round dollar amount
        if total.is_integer():
            points += 50
            # logger.debug(f"Added 50 points for round total: {total}")

        # Rule 3: 25 points if total is a multiple of 0.25
        if total % 0.25 == 0:
            points += 25
            # logger.debug(f"Added 25 points for total being multiple of 0.25: {total}")

        # Rule 4: 5 points for every two items
        item_points = (len(receipt["items"]) // 2) * 5
        points += item_points
        # logger.debug(f"Item count points: {item_points}")

        # Rule 5: If item description length (trimmed) is a multiple of 3
        for item in receipt["items"]:
            desc = item["shortDescription"].strip()
            if len(desc) % 3 == 0:
                price_points = math.ceil(float(item["price"]) * 0.2)
                points += price_points
                # logger.debug(f"Item: {desc} - {price_points} points added")

        # Rule 6: 6 points if the day in purchase date is odd
        purchase_date = datetime.strptime(receipt["purchaseDate"], "%Y-%m-%d").date()
        if purchase_date.day % 2 == 1:
            points += 6
            # logger.debug(f"Added 6 points for odd day: {purchase_date}")

        # Rule 7: 10 points if purchase time is between 2:01 PM and 3:59 PM
        purchase_time = datetime.strptime(receipt["purchaseTime"], "%H:%M").time()
        if (purchase_time.hour == 14 and purchase_time.minute >= 1) or (purchase_time.hour == 15):
            points += 10
            # logger.debug(f"Added 10 points for purchase time: {purchase_time}")

        logger.info(f"Total calculated points: {points}")
        return points

    def get_points(self, receipt_id: str) -> int:
        """Instantly retrieves precomputed points from memory."""        
        points = self.storage.get_points(receipt_id)
        if points is None:
            logger.warning(f"Points not found for receipt ID: {receipt_id}")
        
        return points
