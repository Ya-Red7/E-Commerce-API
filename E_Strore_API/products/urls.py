from django.urls import path
from .views import list_products

urlpatterns = [
    path('products/', list_products, name='list-products'),
]
