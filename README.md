# **Receipt Processing API**

## **Overview**
This is a **FastAPI-based Receipt Processing API** that:
- Accepts receipts via **POST** requests.
- Precomputes points based on defined rules.
- Stores receipts and points in a **thread-safe in-memory store**.
- Provides an **instant retrieval** of receipt points via **GET** requests.
- Designed for **scalability** with dependency injection and Docker support.

---

## **Project Structure**
```
fetch-receipt-processor/
│── app/
│   ├── api/
│   │   ├── routes.py        # FastAPI route definitions
│   ├── models/
│   │   ├── receipt.py       # Pydantic models for validation
│   ├── services/
│   │   ├── receipt_service.py  # Business logic for receipts
│   │   ├── memory_storage.py   # In-memory thread-safe storage
│   ├── main.py              # FastAPI app entry point
│── tests/
│── Dockerfile               # Docker build configuration
│── requirements.txt         # Python dependencies
│── README.md                # Documentation (this file)
```

---

## **Installation & Setup**

---

### **Clone the Repository**
```sh
git clone <repo-url>
cd fetch-receipt-processor
```

## **Running the Application with Docker**

### **1️ Build the Docker Image**
```sh
docker build -t fastapi-receipt-processor .
```

### **2️ Run the Docker Container**
```sh
docker run -p 8000:8000 fastapi-receipt-processor
```

## **Running the Application on local**

### **Install Dependencies**
```sh
pip install -r requirements.txt
```

### **Run the FastAPI Application**
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### **Access the API Documentation**
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc UI:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## **API Endpoints**

### **Process a Receipt**
- **Endpoint:** `POST /receipts/process`
- **Description:** Stores a receipt and computes points instantly.
- **Request Body (JSON):**
```json
{
  "retailer": "Target",
  "purchaseDate": "2024-03-03",
  "purchaseTime": "12:30",
  "items": [
    {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
    {"shortDescription": "Doritos Nacho Cheese", "price": "3.50"}
  ],
  "total": "9.99"
}
```
- **Response (JSON):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "points": 55
}
```

### **Retrieve Points for a Receipt**
- **Endpoint:** `GET /receipts/{id}/points`
- **Description:** Retrieves precomputed points for a given receipt.
- **Response Example (JSON):**
```json
{
  "points": 55
}
```

---

## **Rules for Points Calculation**
| Rule | Description |
|------|-------------|
| **Retailer Name** | 1 point for every alphanumeric character in the retailer name |
| **Round Total** | 50 points if the total is a round dollar amount |
| **Multiple of 0.25** | 25 points if the total is a multiple of 0.25 |
| **Item Count** | 5 points for every two items |
| **Item Description** | If the length of an item description (trimmed) is a multiple of 3, earn `ceil(price * 0.2)` points |
| **Odd Purchase Day** | 6 points if the purchase date is an odd-numbered day |
| **Time Bonus** | 10 points if purchase time is between 2:01 PM and 3:59 PM |

---

## **Contributor**
- **Developer:** Aishwarya Gupta


