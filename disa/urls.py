from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("product_detail/<int:product_id>", views.product_detail, name='product_detail'),
    path("cart_summary/", views.cart_summary, name='cart_summary'),
    path("add_to_cart/", views.add_to_cart, name='add_to_cart'),
    path("update_to_cart/", views.update_to_cart, name='update_to_cart'),
    path("delete_to_cart/", views.delete_to_cart, name='delete_to_cart'),
    path("login", views.user_login, name='contact'),
    path("register", views.user_register, name='register'),
    path("logout", views.user_logout, name='logout'),
]