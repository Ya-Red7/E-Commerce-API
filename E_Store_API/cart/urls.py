from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView, CheckoutView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
