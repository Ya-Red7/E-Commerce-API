from django.urls import path
from .views import list_products, ProductListView, ProductDetailView

urlpatterns = [
    path('products/', list_products, name='list-products'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail')
]
