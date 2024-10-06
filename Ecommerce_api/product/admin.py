from django.contrib import admin
from .models import Product, Review, Order, Category

admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)
