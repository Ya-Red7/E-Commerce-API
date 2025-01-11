📘 E_Store_API - E-Commerce Product API
🔗 Base URL: https://yaredw.pythonanywhere.com/
E_Store_API is a RESTful API built with Django REST Framework (DRF) that enables product management, user authentication, shopping cart functionality, and order processing for an e-commerce platform.
✅ Key Features:
 ✔️ User Authentication (JWT-based login & signup)
 ✔️ Product Management (CRUD operations)
 ✔️ Search & Filtering (name, category, price, stock availability, fuzzy search)
 ✔️ Pagination for large product lists
 ✔️ Shopping Cart & Order Processing (Stock is deducted at checkout)
 ✔️ Reviews & Ratings (Permanent, no edits)
 ✔️ Discounts & Promo Codes (VIP-only promo codes)

📌 Authentication
🔹 User Signup
Endpoint:
POST /api/auth/register/

Request Body:
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword"
}

Response:

{
    “Id”: 1
    "username": "testuser",
    "email": "test@example.com"
}

🔹 User Login (JWT)
Endpoint:
POST /api/auth/login/

Request Body:
{
    "username": "testuser",
    "password": "securepassword"
}

Response:
{
    "refresh": "REFRESH_TOKEN",
    “access”: “YOUR_JWT_TOKEN”
}

📌 Include this token in the Authorization header for all authenticated requests:
Authorization: Bearer YOUR_JWT_TOKEN


📌 Product Management
🔹 Create a Product (Authenticated Users Only)
POST /api/products/create/

Request Body (JSON):
{
     "name": "Air Pod",
    "description": "High--Quality wireless AirPod",
    "price": 299.99,
    "category": "electronics",
    "stock_quantity": 10,
    "image_url": "https://example.com/airpod.jpg"
}

🔹 Get All Products (With Pagination)
GET /api/products/

🔹 Pagination Available:
 ✅ Default page size is 10 items
 ✅ Get next pages with ?page=2, ?page=3
 ✅ Change page size with ?page_size=5
🔹 Filters Available:
 ✅ Search by Name/Category (Fuzzy Search Supported) → /api/products/?search=mouse
 ✅ Filter by Category → /api/products/?category=electronics
 ✅ Filter by Stock → /api/products/?in_stock=true
 ✅ Filter by Price Range → /api/products/?min_price=10&max_price=50
 ✅ Sort by Price or Date Added → /api/products/?ordering=price

📌 Reviews & Ratings
🔹 Submit a Review (Permanent, No Edits)
POST /api/review/

Request Body:
{
    "product_id": 1,
    "rating": 5,
    "comment": "Excellent product!"
}

Response:
{
    "message": "Review submitted successfully!"
}

📌 Reviews cannot be edited or deleted once submitted.

📌 Cart & Order Management
🔹 Place an Order (Automatically Adds to Cart)
POST /api/order/

Request Body:
{
    "product_id": 1,
    "quantity": 2
}

Response:
{
    "message": "Order placed successfully!",
    "total_price": 59.98
}

✅ Stock is not deducted at this step.
🔹 View Cart (Total Price Included)
GET /api/cart/

Response:
{
    "items": [
        {
            “Id”: 1,
            "product_name": "Wireless Mouse",
            "quantity": 2,
            "total_price": 59.98
        }
    ],
    "total_price": 59.98
}

✅ Cart total price reflects only the items currently in the cart.
🔹 Remove Product from Cart (Stock is Restored)
DELETE /api/cart/remove/1/

Response:
{
    "message": "Product removed from cart"
}

✅ Stock is restored to its previous value when a product is removed.
🔹 Checkout (Deducts Stock & Clears Cart)
POST /api/cart/checkout/

Response:
{
    "message": "Checkout successful",
    "total_price": 99.98
}

✅ Stock is deducted only at this step, ensuring accurate inventory management.

📌 Discounts & Promo Codes
Percentage-based discounts apply to all users.
Promo codes are only available for VIP customers.
🔹 Example: Applying a Discount
GET /api/products/1/

Response:
{
    "name": "Wireless Mouse",
    "original_price": 29.99,
    "discount_percentage": 10,
    "final_price": 26.99
}


📌 Contributors
👨‍💻 Developed by: Yared Wondatir
