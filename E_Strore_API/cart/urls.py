# cart/urls.py
from django.urls import path
from .views import CartListView, AddToCartView, RemoveFromCartView

urlpatterns = [
    path('view/', CartListView.as_view(), name='cart_view'),
    path('add/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]
