from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Product, Order, Category
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSetTests(APITestCase):
    def setUp(self):
        # Create a test user and an admin user for authentication
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.admin_user = get_user_model().objects.create_superuser(username='admin', password='adminpass')
        
        # Generate a token for the test user for authentication in requests
        self.token = str(RefreshToken.for_user(self.user).access_token)
        
    def test_create_user(self):
        # Test creating a new user through the API
        user_data = {
            'username': 'newuser', 
            'password': 'newpass', 
            'email': 'newuser@example.com'
        }
        response = self.client.post(reverse('user-list'), user_data)
                
        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user(self):
        # Authenticate the client using the test user's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Attempt to retrieve the test user details
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
                
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_unauthenticated(self):
        # Attempt to retrieve the user details without authentication
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        
        # Assert that the response status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductViewSetTests(APITestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        
        # Create a test category to associate with products
        self.category = Category.objects.create(name='Test Category')
        
        # Generate a token for the test user for authentication in requests
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_list_products(self):
        # Attempt to retrieve the list of products
        response = self.client.get(reverse('product-list'))
        
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        # Attempt to create a new product through the API
        response = self.client.post(reverse('product-list'), {
            'name': 'New Product',
            'price': 15.99,
            'stock_quantity': 50,
            'category': self.category.id,
            'image_url': 'https://example.com/image.jpg',
            'description': 'This is a great product.'
        })
        
        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_unauthenticated(self):
        # Log out the authenticated user to simulate an unauthenticated request
        self.client.logout()  
        
        # Attempt to create a product without authentication
        response = self.client.post(reverse('product-list'), {
            'name': 'New Product',
            'price': 15.99,
            'stock_quantity': 50,
            'category': self.category.id
        })
        
        # Assert that the response status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderViewSetTests(APITestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        
        # Create a test category to associate with products
        self.category = Category.objects.create(name='Test Category')  
        
        # Create a test product to place orders
        self.product = Product.objects.create(
            name='Test Product', 
            price=10.99, 
            stock_quantity=100, 
            category=self.category
        )
        
        # Generate a token for the test user for authentication in requests
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_order(self):
        # Attempt to create a new order through the API
        response = self.client.post(reverse('order-list'), {
            'user': self.user.id,  # ID of the user placing the order
            'product': self.product.id,  # ID of the product being ordered
            'quantity': 2,  # Quantity of the product to order
        })
        
        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_unauthenticated(self):
        # Log out the authenticated user to simulate an unauthenticated request
        self.client.logout()
        
        # Attempt to create an order without authentication
        response = self.client.post(reverse('order-list'), {
            'user': self.user.id,
            'product': self.product.id,
            'quantity': 2
        })
        
        # Assert that the response status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewViewSetTests(APITestCase):
    def setUp(self):
        # Create a test category to associate with products
        self.category = Category.objects.create(name='Test Category')
        
        # Create a test user for authentication
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        
        # Generate a token for the test user for authentication in requests
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create a test product to review
        self.product = Product.objects.create(
            name='Test Product',
            price=10.99,
            image_url='http://example.com/image.jpg',
            description='Test Product Description',
            stock_quantity=100,
            category=self.category
        )

    def test_create_review(self):
        # Attempt to create a review for the test product
        response = self.client.post(
            reverse('review-list'),  # Adjust the URL to your reviews endpoint
            data={
                'product': self.product.id,  # The ID of the product being reviewed
                'user': self.user.id,  # Include the user field to associate the review with the user
                'rating': 5,  # The rating given by the user
                'comment': 'Great product!'  # The review comment
            }
        )
        
        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_review_unauthenticated(self):
        # Log out the authenticated user to simulate an unauthenticated request
        self.client.logout()  
        
        # Attempt to create a review without authentication
        response = self.client.post(
            reverse('review-list'),
            data={
                'product': self.product.id,  # The ID of the product being reviewed
                'rating': 5,  # The rating given by the user
                'comment': 'Great product!'  # The review comment
            }
        )
        
        # Assert that the response status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        # Create a test category for listing
        self.category = Category.objects.create(name='Test Category')

    def test_list_categories(self):
        # Attempt to retrieve the list of categories
        response = self.client.get(reverse('category-list'))
        
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
