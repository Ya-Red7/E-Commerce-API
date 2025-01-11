from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.conf import settings

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('home', 'Home'),
        ('beauty', 'Beauty'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    stock_quantity = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Discount Fields
    discount_percentage = models.PositiveIntegerField(default=0)  # Percentage-based discount
    promo_code = models.CharField(max_length=20, blank=True, null=True)  # VIP-only promo codes
    
    def average_rating(self):
        return self.reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or None
    
    def apply_discount(self):
        """Calculates final price after applying the percentage discount."""
        discount_amount = (self.price * self.discount_percentage) / 100
        return self.price - discount_amount
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        """Automatically decrease stock when an order is placed."""
        if self.product.stock_quantity >= self.quantity:
            self.total_price = self.product.apply_discount() * self.quantity
            self.product.stock_quantity -= self.quantity
            self.product.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError("Not enough stock available.")
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.product.name}"

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}⭐"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username