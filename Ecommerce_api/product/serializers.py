from rest_framework import serializers
from .models import Product , Order , Review, Category
from django.contrib.auth.models import User

# ProductSerializer is a class that is responsible for converting a Product model instance into a format that can be serialized into JSON format
class ProductSerializer(serializers.ModelSerializer):
    # The Meta class is where we define the fields that we want to include from the Product model and how they should be serialized
    class Meta:
        model = Product
        # We want to include all the fields from the Product model
        fields = '__all__'

# This class is used to serialize User objects into JSON format.
class UserSerializer(serializers.ModelSerializer):
    # The Meta class is where we define the fields that we want to include from the User model and how they should be serialized
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Overriding the create method to hash the password
    def create(self, validated_data):
        """
        This method is called when we want to create a new User object.
        It hashes the password before saving it to the database.
        """
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    # Overriding the update method to hash the password
    def update(self, instance, validated_data):
        """
        This method is called when we want to update an existing User object.
        It hashes the password before saving it to the database if the password has been changed.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)  # Hash the new password
        instance.save()
        return instance
class OrderSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize Order objects into JSON format and vice versa.
    """
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        """
        This method is called when we want to create a new Order object.
        The stock quantity reduction will happen in the save method of the model
        """
        return Order.objects.create(**validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize Review objects into JSON format and vice versa.
    """
    class Meta:
        model = Review
        fields = '__all__' # This will include all the fields in the Review model
    """
    The fields attribute is a special attribute that can be used to select which fields to include in the output.
    In this case, we are including all the fields in the Review model.
    """
class CategorySirializers(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields=["id","name"]
