from knox import views as knox_views
from django.urls import path
from .views import RegistrationAPI,CartItemCreateAPIView,CartItemAPIView,CartAPIView, CartItemView, LoginAPI ,ProductAPIView,ShopProductAPIView, ProductDetailAPIView,ShopAPIView

urlpatterns = [
    path('seller/api/auth/signup', RegistrationAPI.as_view()),
    path('seller/api/auth/login', LoginAPI.as_view()),
    
    path('products', ProductAPIView.as_view()),
    path('product/<int:id>', ProductDetailAPIView.as_view()),

    path('api/auth/createShop', ShopAPIView.as_view()),

    path('shop/product/<int:id>', ShopProductAPIView.as_view()),

    path("api/cart/<int:id>", CartAPIView.as_view()), #tao, xem gio hang rong

    path('cart-item/create', CartItemCreateAPIView.as_view()),
    
    path("cart-item/update/<int:id>", CartItemAPIView.as_view()),


    path("cart/detail/<int:id>", CartItemView.as_view()), # xem items trong cart



]