# **📘 E_Store_API - E-Commerce Product API**  

🔗 **Base URL:** `https://yaredw.pythonanywhere.com/`  

E_Store_API is a RESTful API built with **Django REST Framework (DRF)** that enables **product management, user authentication, shopping cart functionality, and order processing** for an e-commerce platform.  

✅ **Key Features:**  
✔️ **User Authentication (JWT-based login & signup)**  
✔️ **Product Management (CRUD operations)**  
✔️ **Search & Filtering (name, category, price, stock availability, fuzzy search)**  
✔️ **Pagination for large product lists**  
✔️ **Shopping Cart & Order Processing (Stock is deducted at checkout)**  
✔️ **Reviews & Ratings (Permanent, no edits)**  
✔️ **Discounts & Promo Codes (VIP-only promo codes)**  

---

## **📌 Authentication**
### **🔹 User Signup**
**Endpoint:**  
```http
POST /api/auth/register/
```
**Request Body:**
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword"
}
```
**Response:**
```json
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"

}
```

### **🔹 User Login (JWT)**
**Endpoint:**  
```http
POST /api/auth/login/
```
**Request Body:**
```json
{
    "username": "testuser",
    "password": "securepassword"
}
```
**Response:**
```json
{
    "refresh": "REFRESH_TOKEN",
    "access": "YOUR_JWT_TOKEN"

}
```
📌 **Include this token in the `Authorization` header for all authenticated requests:**  
```
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## **📌 Product Management**  
### **🔹 Create a Product (Authenticated Users Only)**
```http
POST /api/products/create/
```
**Request Body (JSON):**
```json
{
     "name": "Air Pod",
    "description": "High--Quality wireless AirPod",
    "price": 299.99,
    "category": "electronics",
    "stock_quantity": 10,
    "image_url": "https://example.com/airpod.jpg"
}
```

### **🔹 Get All Products (With Pagination)**
```http
GET /api/products/
```

### **🔹 GET a specific product**
```http
GET /api/products/{id}/
```


🔹 **Pagination Available:**  
✅ **Default page size is 10 items**  
✅ **Get next pages with `?page=2`, `?page=3`**  
✅ **Change page size with `?page_size=5`**  

🔹 **Filters Available:**  
✅ **Search by Name/Category (Fuzzy Search Supported)** → `/api/products/?search=mouse`  
✅ **Filter by Category** → `/api/products/?category=electronics`  
✅ **Filter by Stock** → `/api/products/?in_stock=true`  
✅ **Filter by Price Range** → `/api/products/?min_price=10&max_price=50`  
✅ **Sort by Price or Date Added** → `/api/products/?ordering=price`  

---

## **📌 Reviews & Ratings**
### **🔹 Submit a Review (Permanent, No Edits)**
```http
POST /api/review/
```
**Request Body:**
```json
{
    "product_id": 1,
    "rating": 5,
    "comment": "Excellent product!"
}
```
**Response:**
```json
{
    "message": "Review submitted successfully!"
}
```
📌 **Reviews cannot be edited or deleted once submitted.**  

---

## **📌 Cart & Order Management**  
### **🔹 Place an Order (Automatically Adds to Cart)**
```http
POST /api/order/
```
**Request Body:**
```json
{
    "product_id": 1,
    "quantity": 2
}
```
**Response:**
```json
{
    "message": "Order placed successfully!",
    "total_price": 59.98
}
```
✅ **Stock is not deducted at this step.**  

### **🔹 View Cart (Total Price Included)**
```http
GET /api/cart/
```
**Response:**
```json
{
    "items": [
        {
            "id": 1,
            "product_name": "Wireless Mouse",
            "quantity": 2,
            "total_price": 59.98
        }
    ],
    "total_price": 59.98
}
```
✅ **Cart total price reflects only the items currently in the cart.**  

### **🔹 Remove Product from Cart (Stock is Restored)**
```http
DELETE /api/cart/remove/1/
```
**Response:**
```json
{
    "message": "Product removed from cart"
}
```
✅ **Stock is restored to its previous value when a product is removed.**  

### **🔹 Checkout (Deducts Stock & Clears Cart)**
```http
POST /api/cart/checkout/
```
**Response:**
```json
{
    "message": "Checkout successful",
    "total_price": 99.98
}
```
✅ **Stock is deducted only at this step, ensuring accurate inventory management.**  

---

## **📌 Discounts & Promo Codes**
- **Percentage-based discounts apply to all users.**  
- **Promo codes are only available for VIP customers.**  



## **📌 Contributors**
👨‍💻 **Developed by:** Yared Wondatir  
