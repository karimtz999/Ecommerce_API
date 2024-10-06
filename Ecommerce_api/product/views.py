from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from .models import Product, Order, Review, Category    
from rest_framework.response import Response
from .serializers import (
    ProductSerializer,
    UserSerializer,
    OrderSerializer,
    ReviewSerializer,
    CategorySerializer,
)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from django_filters import rest_framework as django_filters
from rest_framework_simplejwt.authentication import JWTAuthentication


# --------------------
# USER VIEWSET
# --------------------
class UserViewSet(viewsets.ModelViewSet):

    # Handles CRUD operations for users. Only authenticated users can view, update, or delete a user,
    # but anyone can create a new account (POST action).
    authentication_classes = [JWTAuthentication]  # Token-based authentication using JWT
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can perform other actions

    def get_permissions(self):
        """
        Allow non-authenticated users to create an account (POST),
        but require authentication for other actions (GET, PUT, DELETE).
        """
        if self.action == "create":
            return []  # No authentication required for user registration (POST)
        return [IsAuthenticated()]  # Require authentication for other actions

    def get_queryset(self):
        """
        Return a queryset depending on the user's role:
        - Admin users can view all users.
        - Regular users can only view their own account.
        """
        if self.request.user.is_staff:  # Check if the user is an admin
            return User.objects.all()  # Admin users can see all users
        return User.objects.filter(id=self.request.user.id)  # Regular users can only see their own data

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        # Handle password update securely
        if "password" in request.data:
            user.set_password(request.data["password"])  # Use set_password to hash the password
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Allows only admin users to delete any user, while regular users can only delete their own account.
        """
        user = self.get_object()
        if request.user.is_staff or request.user == user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "You don't have permission to delete this user."},
            status=status.HTTP_403_FORBIDDEN
        )


# --------------------
# PRODUCT FILTER
# --------------------
class ProductFilter(django_filters.FilterSet):
    """
    Provides filtering options for products based on various criteria such as price range,
    category, and stock status.
    """
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte"
    )  # Minimum price filter
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte"
    )  # Maximum price filter
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all()
    )  # Filter by category
    in_stock = django_filters.BooleanFilter(
        field_name="stock_quantity", lookup_expr="gt", label="In Stock"
    )  # Filter products that are in stock

    class Meta:
        model = Product
        fields = ["category", "min_price", "max_price", "in_stock"]

# --------------------
# PRODUCT VIEWSET
# --------------------
class ProductViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for products. Allows read-only access for unauthenticated users
    and enables filtering and searching by category name.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all().order_by('name')    # Optimize query by using select_related for foreign keys

    # Enable filtering and search by product name and category
    filterset_class = ProductFilter
    search_fields = ['name', 'category__name']  # Search by product name or category name
    filter_backends = [django_filters.DjangoFilterBackend]

    def get_queryset(self):
        """
        Retrieves the list of products with optimized queries. This method can be extended
        to apply additional filters if needed.
        """
        return super().get_queryset()


# --------------------
# ORDER VIEWSET
# --------------------
class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin/staff users to update or delete orders.
    Regular users can view (GET) and create (POST) their own orders, but cannot modify or delete them.
    """
    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the requested action.
        """
        # All authenticated users can view or create orders
        if request.method in ['GET', 'HEAD', 'OPTIONS', 'POST']:
            return request.user.is_authenticated

        # Only admin/staff users can update or delete orders
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to only allow owners of the object to view their orders.
        Admin/staff users can modify (PUT, DELETE) any order.
        """
        # Allow GET for the owner of the order
        if request.method == 'GET' and obj.user == request.user:
            return True

        # Allow PUT/DELETE only for admin/staff or the owner
        if request.method in ['PUT', 'DELETE']:
            # Admin/staff users can modify or delete any order
            if request.user.is_staff:
                return True

            # Regular users can only modify or delete their own orders
            return obj.user == request.user

        return False  # Deny access by default


class OrderViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for orders.
    Provides token-based authentication and allows authenticated users to view and create orders.
    Admin/staff users can modify or delete any order.
    """
    authentication_classes = [JWTAuthentication]  # Token-based authentication using JWT
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]  # Admin/staff have full control; regular users have limited access
    serializer_class = OrderSerializer
    def get_queryset(self):
        """
        Allows users to see only their own orders. Admin users can see all orders.
        Optimizes the query by using select_related for foreign keys 
        and prefetch_related for related objects.
        """
        if self.request.user.is_staff:
            return Order.objects.select_related('user').all().order_by('id')
        return Order.objects.filter(user=self.request.user).select_related('user')


# --------------------
# REVIEW VIEWSET
# --------------------
class ReviewViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for reviews. 
    Only authenticated users can post a review, and the user who created the review is automatically assigned.
    """
    queryset = Review.objects.all().order_by('id')  # Fetch all reviews
    serializer_class = ReviewSerializer  # Serializer for converting review objects to and from JSON
    permission_classes = [
        IsAuthenticated  # Only authenticated users can perform actions
    ]

    def perform_create(self, serializer):
        """
        Automatically assign the user who created the review.
        This ensures that the review is linked to the user.
        """
        serializer.save(user=self.request.user)  # Save the review with the current user as the reviewer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for categories. Provides read-only access for unauthenticated users.
    """
    authentication_classes = [JWTAuthentication]  # Token-based authentication using JWT
    permission_classes = [IsAuthenticatedOrReadOnly ]  # Unauthenticated users can only view categories
    serializer_class = CategorySerializer  # Serializer for converting category objects to/from JSON
    queryset = Category.objects.all().order_by('id')  # Fetch all categories

    def get_queryset(self):
        """
        Return all categories. Additional filters can be added here if needed.
        """
        return Category.objects.all().order_by('id')