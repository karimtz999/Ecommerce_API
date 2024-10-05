from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from .models import Product, Order, Review, Category

class UserViewSetTests(APITestCase):
    """
    Unit tests for UserViewSet to ensure user registration and account retrieval behave as expected.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')

    def test_create_user(self):
        """
        Test creating a new user (POST).
        """
        response = self.client.post(reverse('user-list'), {
            'username': 'newuser',
            'password': 'newpass'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user_as_authenticated(self):
        """
        Test retrieving user details (GET) when authenticated.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_as_unauthenticated(self):
        """
        Test retrieving user details (GET) when not authenticated.
        """
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProductViewSetTests(APITestCase):
    """
    Unit tests for ProductViewSet to ensure product retrieval, creation, and access control behave as expected.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=10.99, stock_quantity=100, category=self.category)

    def test_list_products(self):
        """
        Test listing products (GET).
        """
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_as_authenticated(self):
        """
        Test creating a new product (POST) as an authenticated user.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('product-list'), {
            'name': 'New Product',
            'price': 15.99,
            'stock_quantity': 50,
            'category': self.category.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_as_unauthenticated(self):
        """
        Test creating a new product (POST) as an unauthenticated user.
        """
        response = self.client.post(reverse('product-list'), {
            'name': 'New Product',
            'price': 15.99,
            'stock_quantity': 50,
            'category': self.category.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderViewSetTests(APITestCase):
    """
    Unit tests for OrderViewSet to ensure order creation and access control behave as expected.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.product = Product.objects.create(name='Test Product', price=10.99, stock_quantity=100)
        self.order = Order.objects.create(user=self.user)

    def test_create_order_as_authenticated(self):
        """
        Test creating a new order (POST) as an authenticated user.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('order-list'), {
            'user': self.user.id,
            'product': self.product.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_as_unauthenticated(self):
        """
        Test creating a new order (POST) as an unauthenticated user.
        """
        response = self.client.post(reverse('order-list'), {
            'user': self.user.id,
            'product': self.product.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_order_as_authenticated_user(self):
        """
        Test retrieving an order (GET) as an authenticated user.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('order-detail', args=[self.order.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_as_unauthenticated(self):
        """
        Test retrieving an order (GET) as an unauthenticated user.
        """
        response = self.client.get(reverse('order-detail', args=[self.order.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewViewSetTests(APITestCase):
    """
    Unit tests for ReviewViewSet to ensure review creation and access control behave as expected.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(name='Test Product', price=10.99, stock_quantity=100)

    def test_create_review_as_authenticated(self):
        """
        Test creating a new review (POST) as an authenticated user.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('review-list'), {
            'product': self.product.id,
            'rating': 5,
            'comment': 'Great product!'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_review_as_unauthenticated(self):
        """
        Test creating a new review (POST) as an unauthenticated user.
        """
        response = self.client.post(reverse('review-list'), {
            'product': self.product.id,
            'rating': 5,
            'comment': 'Great product!'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
