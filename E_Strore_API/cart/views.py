# cart/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializers import CartSerializer

class CartListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can view their cart

class AddToCartView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can add items to their cart

class RemoveFromCartView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can remove items from their cart
