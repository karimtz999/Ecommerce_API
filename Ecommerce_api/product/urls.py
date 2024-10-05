from rest_framework.routers import DefaultRouter # this module provide easyer way to handel endpoints creation
from .views import ProductViewSet , UserViewSet , OrderViewSet , ReviewViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path


router = DefaultRouter() # for django API we use DefaultRouter instead of adding it manualy to urlpttern list
router.register(r'products', ProductViewSet, basename='user') # this how we register a urlpaterne by ('name for the url route(can be any name)', the viewet that handel request of our end point)
router.register(r'users',UserViewSet, basename='product') #the same her for user end point
router.register(r'orders', OrderViewSet, basename='order') # here i added a route for the order views 
router.register(r'reviews', ReviewViewSet, basename='review') # here i added a route for the review views

urlpatterns = router.urls + [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # for login using jwt , access token and refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # We use this route to obtain a new access token when the current one expires
]