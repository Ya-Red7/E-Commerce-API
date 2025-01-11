from django.contrib.auth import authenticate
from rest_framework import generics, status, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import CustomUser, Product, Order, Review
from .serializers import RegisterSerializer, LoginSerializer, ProductSerializer, ProductSerializer, ReviewSerializer, OrderSerializer
from cart.models import Cart, CartItem

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Allow access to all users but restrict updates to owners."""
        product = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and product.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this product.")
        return product

class ProductPagination(PageNumberPagination):
    page_size = 10  # Set default page size
    page_size_query_param = 'page_size'  # Allow client to specify page size
    max_page_size = 50  # Prevent excessive page sizes


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'category']
    ordering_fields = ['price', 'created_at']

    pagination_class = ProductPagination
    def get_queryset(self):
        queryset = Product.objects.all()
        
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
                queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
            except ValueError:
                raise ValidationError({"error": "Invalid price value. Prices must be numbers."})

        in_stock = self.request.query_params.get('in_stock', None)
        if in_stock:
            if in_stock.lower() == 'true':
                queryset = queryset.filter(stock_quantity__gt=0)
            elif in_stock.lower() == 'false':
                queryset = queryset.filter(stock_quantity=0)
            else:
                raise ValidationError({"error": "Invalid value. Value must be boolean."})
        return queryset

    
class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity',"1")

        try:
            quantity = int(quantity)
            product = Product.objects.get(id=product_id)

            # Check if enough stock is available
            if product.stock_quantity < quantity:
                return Response({"error": "Not enough stock available."}, status=status.HTTP_400_BAD_REQUEST)
            
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Add product to cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            current_order_price = product.apply_discount() * quantity
            #order = Order.objects.create(user=request.user, product=product, quantity=quantity)
            return Response({"message": "Order placed successfully!", "total_price": current_order_price}, status=status.HTTP_201_CREATED)
        
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        rating = int(request.data.get('rating'))
        comment = request.data.get('comment', '')

        try:
            product = Product.objects.get(id=product_id)

            # Prevent duplicate reviews
            if Review.objects.filter(user=request.user, product=product).exists():
                return Response({"error": "You have already reviewed this product."}, status=status.HTTP_400_BAD_REQUEST)

            review = Review.objects.create(user=request.user, product=product, rating=rating, comment=comment)
            return Response({"message": "Review submitted successfully!"}, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid rating."}, status=status.HTTP_400_BAD_REQUEST)
