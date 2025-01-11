from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404

class CartView(APIView):
    """Retrieve the current user's cart."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddToCartView(APIView):
    """Add a product to the cart."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        
        for item in cart.items.all():
            if item.product.stock_quantity < item.quantity:
                return Response(
                    {"message": f"Not enough stock for {item.product.name}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            #item.product.stock_quantity -= item.quantity
            #item.product.save()
        

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response({"message": "Product added to cart"}, status=status.HTTP_201_CREATED)

class RemoveFromCartView(APIView):
    """Remove a product from the cart."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, product_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)


        cart_item.delete()
        return Response({"message": "Product removed from cart"}, status=status.HTTP_200_OK)

class CheckoutView(APIView):
    """Convert cart items into an order and deduct stock."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            return Response({"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        

        cart.items.all().delete()  # Clear cart after checkout
        return Response({"message": "Checkout successful"}, status=status.HTTP_200_OK)
