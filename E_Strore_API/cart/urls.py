from django.urls import path
from .views import add_to_cart

urlpatterns = [
    path('cart/add/', add_to_cart, name='add-to-cart'),
]
