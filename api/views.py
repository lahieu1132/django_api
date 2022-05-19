from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from .models  import Product, Shop, Cart, CartItem
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer,ShopSerializer, ProductSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CartItemSerializer, CartItemUpdateSerializer, CartSerializer
from rest_framework import status, authentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)

# Create your views here.
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
    
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ProductAPIView(APIView):

    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many = True)
        return Response(serializer.data)
    def post(self, request):
        serializer = ProductSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = self.get_object(id)
        data = JSONParser().parse(request)
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ShopAPIView(APIView):

    def get(self, request):
        shop = Shop.objects.all().filter(user_id= request.data["id"])
        serializer = ShopSerializer(shop, many = True)
        return Response(serializer.data)
    def post(self, request):
        serializer = ShopSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopProductAPIView(APIView):
    def get(self, request):
        product = Product.objects.all().filter(shop_id = request.data["id"])
        serializer = ProductSerializer(product, many = True)
        return Response(serializer.data)

class CartAPIView(APIView):

    def get(self, request):
        cart = Cart.objects.all().filter(user= request.data["id"])
        serializer = CartSerializer(cart, many = True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CartSerializer(data = request.data, many = True)

        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemCreateAPIView(APIView):

    def post(self, request):
        cart = Cart.objects.get(user = request.data['cart'])
        product = Product.objects.get(id = request.data['product'])
        cart.total = int(cart.total) + int(request.data['quantity'])*int(product.price)
        cart.save()
        serializer = CartItemSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemAPIView(APIView):
    def get_object(self, id):
        try:
            return CartItem.objects.get(id=id)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def get(self, request, id):
        cartItem = self.get_object(id)
        serializer = CartItemSerializer(cartItem)
        return Response(serializer.data)

    def put(self, request, id):
        cartItem = self.get_object(id)
        cart = Cart.objects.get(user = request.data["cart"])
        product = Product.objects.get(id = request.data['product'])
        if (int(request.data['quantity']) - int(product.quantity)) > 0:
            cart.total = int(cart.total) + (int(request.data['quantity']) - int(product.quantity))*int(product.price)
        else:
            cart.total = int(cart.total) - (int(request.data['quantity']) - int(product.quantity))*int(product.price)
        cart.save()
        if request.data["quantity"] != 0:
            data = JSONParser().parse(request)
            serializer = CartItemSerializer(cartItem, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            cartItem.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemView(APIView):
    def get_object(self, id):
        try:
            return CartItem.objects.all().filter(cart=id)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def get(self, request, id):
        cartItems = self.get_object(id)
        # products = Product.objects.all().filter(id = cartItem.)
        serializer = CartItemSerializer(cartItems, many = True)
        productID = []
        for cart_item in serializer.data:
            productID.append(cart_item["product"])
        products = Product.objects.filter(id__in = productID)
        print(products)
        productsSerial = ProductSerializer(products, many=True)
        return Response({
            "items": serializer.data,
            "products": productsSerial.data
        })

# class CartItemAPIView(ListCreateAPIView):
#     serializer_class = CartItemSerializer

#     def get_queryset(self):
#         user = self.request.user
#         print(self.request.user)
#         queryset = CartItem.objects.filter(cart__user=request.data['user'])
#         return queryset

#     def create(self, request, *args, **kwargs):
#         user = request.user
#         cart = get_object_or_404(Cart, user=request.data['user'])
#         if "product" in request.data: 
#             product = get_object_or_404(Product, pk=request.data["product"])
        
#         current_item = CartItem.objects.filter(cart=cart, product=product)


#         if current_item.count() > 0:
#             raise NotAcceptable("You already have this item in your shopping cart")

#         try:
#             quantity = int(request.data["quantity"])
#         except Exception as e:
#             raise ValidationError("Please Enter Your Quantity")

#         if quantity > product.quantity:
#             raise NotAcceptable("You order quantity more than the seller have")

#         cart_item = CartItem(cart=cart, product=product, quantity=quantity)
#         cart_item.save()
#         serializer = CartItemSerializer(cart_item)
#         total = float(product.price) * float(quantity)
#         cart.total = total
#         cart.save()


#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CartItemView(RetrieveUpdateDestroyAPIView):
#     serializer_class = CartItemSerializer
#     # method_serializer_classes = {
#     #     ('PUT',): CartItemUpdateSerializer
#     # }
#     queryset = CartItem.objects.all()

#     def retrieve(self, request, *args, **kwargs):
#         cart_item = self.get_object()
#         # if cart_item.cart.user != request.user:
#         #     raise PermissionDenied("Sorry this cart not belong to you")
#         serializer = self.get_serializer(cart_item)
#         return Response(serializer.data)

#     def update(self, request, *args, **kwargs):
#         cart_item = self.get_object()
#         # cart = Cart.objects.get(id = request.data['user'])
#         product = get_object_or_404(Product, pk=request.data["product"])
#         productss = Product.objects.all()
#         print("tset",productss)
#         # if cart_item.cart != request.data["user"]:
#         #     raise PermissionDenied("Sorry this cart not belong to you")

#         try:
#             quantity = int(request.data["quantity"])
#         except Exception as e:
#             raise ValidationError("Please, input vaild quantity")

#         if quantity > product.quantity:
#             raise NotAcceptable("Your order quantity more than the seller have")

#         serializer = CartItemUpdateSerializer(cart_item, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         cart_item = self.get_object()
#         # if cart_item.cart.user != request.user:
#         #     raise PermissionDenied("Sorry this cart not belong to you")
#         cart_item.delete()

#         return Response(
#             {"detail": _("your item has been deleted.")},
#             status=status.HTTP_204_NO_CONTENT,
#         )

