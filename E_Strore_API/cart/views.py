from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from products.models import Product

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """
    Endpoint to add a product to the cart.
    """
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    try:
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()

        return Response({
            "message": "Product added to cart successfully.",
            "product_id": product.id,
            "quantity": cart_item.quantity
        })
    except Product.DoesNotExist:
        return Response({"error": "Product does not exist."}, status=404)
