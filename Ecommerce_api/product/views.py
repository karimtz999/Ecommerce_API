from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Order, Review, Category
from .serializers import (
    ProductSerializer,
    UserSerializer,
    OrderSerializer,
    ReviewSerializer,
    CategorySirializers,
)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission 
from django_filters import rest_framework as django_filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination


# --------------------
# USER VIEWSET
# --------------------
class UserViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for users. Only authenticated users can view, update, or delete a user,
    but anyone can create a new account (POST action).
    """
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


# --------------------
# PRODUCT FILTER
# --------------------
class ProductFilter(django_filters.FilterSet):

    # Filters for products based on price range, category, and stock status.

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


class ProductPagination(PageNumberPagination):
    page_size = 10  # Adjust based on your needs
# --------------------
# PRODUCT VIEWSET
# --------------------
class ProductViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for products.
    Provides token-based authentication and allows read-only access to unauthenticated users.
    Implements search functionality by product name and category.
    """
    
    authentication_classes = [JWTAuthentication]  # Token-based authentication using JWT
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only access for unauthenticated users
    serializer_class = ProductSerializer
    search_fields = ['name', 'category__name']  # Enables search by product name and category name
    filterset_class = ProductFilter  # Apply product filter
    pagination_class = ProductPagination

    # Define allowed ordering fields
    ordering_fields = ['price', 'name']  # Allow ordering by price or name
    ordering = ['name']  # Default ordering, can be adjusted

    def get_queryset(self):
        """
        Optimizes the query by using select_related for foreign keys 
        and prefetch_related for many-to-many relationships to reduce database hits.
        """
        queryset = Product.objects.select_related('category').all()  # Assuming 'tags' is a many-to-many relationship
        return queryset


# --------------------
# ORDER VIEWSET
# --------------------
from rest_framework.permissions import BasePermission

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
    pagination_class = ProductPagination  # Add pagination to handle large datasets

    def get_queryset(self):
        """
        Allows users to see only their own orders. Admin users can see all orders.
        Optimizes the query by using select_related for foreign keys 
        and prefetch_related for related objects.
        """
        if self.request.user.is_staff:
            return Order.objects.select_related('user').all()  # Assuming 'order_items' is a related name for items in the order
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('order_items')
# REVIEW VIEWSET
# --------------------
class ReviewViewSet(viewsets.ModelViewSet):

    # Handles CRUD operations for reviews. Only authenticated users can post a review, and the user who created the review is automatically assigned.

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Only authenticated users can perform actions

    def perform_create(self, serializer):
        """
        Automatically assign the user who created the review.
        """
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for categories. Provides read-only access for unauthenticated users.
    """
    authentication_classes = [JWTAuthentication]  # Token-based authentication using JWT
    permission_classes = [IsAuthenticatedOrReadOnly]  # Unauthenticated users can only view categories
    serializer_class = CategorySirializers  # Serializer for converting category objects to/from JSON
    queryset = Category.objects.all()  # Fetch all categories

    def get_queryset(self):
        """
        Return all categories. Additional filters can be added here if needed.
        """
        return Category.objects.all()