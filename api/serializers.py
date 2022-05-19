from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Shop, Product , Cart, CartItem
from django.contrib.auth import authenticate

# User Serializer
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password' )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], None, validated_data['password'])
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "title",
            "seller",
            "quantity",
            "price",
            "image",
        )


class CartItemSerializer(serializers.ModelSerializer):
    # product = CartProductSerializer(required=False)
    class Meta:
        model = CartItem
        fields = ("__all__")


class CartItemMiniSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ("product", "quantity")


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("product", "quantity")