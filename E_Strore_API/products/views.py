from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics, permissions

@api_view(['GET'])
def list_products(request):
    """
    Endpoint to fetch all available products.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can view or create products

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can view or update products