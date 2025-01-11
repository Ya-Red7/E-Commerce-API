from django.urls import path
from .views import RegisterView, LoginView, ProductListCreateView, ProductDetailView, ProductListView, CreateOrderView, CreateReviewView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/create/', ProductListCreateView.as_view(), name='product-create'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('order/', CreateOrderView.as_view(), name='create-order'),
    path('review/', CreateReviewView.as_view(), name='create-review'),
]
