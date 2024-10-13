from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# this class for storig category instences with all data required
class Category(models.Model):
    name = models.CharField(max_length=255)  # name of category is a required field

    def __str__(self):
        return self.name

# this tabel for storig product instences with all data required
class Product(models.Model):
    name = models.CharField(
        max_length=100, blank=False, null=False
    )  # name of the product
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )  # price of product we did add (blank and null) for validation
    image_url = (
        models.URLField()
    )  # a url field (thats mean that the images are not stored localy in our server but accesed using a url)
    description = models.TextField()
    stock_quantity = models.PositiveIntegerField(
        default=0, blank=False, null=False
    )  # we set the default value to 0
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# this class for storig user instences with all data required
class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # the name of user who placed the order
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE
    )  # the product that was ordered
    quantity = models.PositiveIntegerField()  # Number of units ordered
    ordered_at = models.DateTimeField(
        auto_now_add=True
    )  # Date and time when the order was placed

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    # the save method to reduce the stock quantity after order is placed and to save the order
    def save(self, *args, **kwargs):
        # Check if there's enough stock before placing the order
        if self.product.stock_quantity < self.quantity:
            raise ValidationError(
                f"Not enough stock for {self.product.name}. Available stock is {self.product.stock_quantity}."
            )

        # Reduce stock quantity after order is placed
        self.product.stock_quantity -= self.quantity
        self.product.save()

        super().save(*args, **kwargs)


# this class for storig review instences with all data required
class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )  # related_name is used to avoid naming conflict
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.product.name}"


