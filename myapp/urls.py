from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpResponseNotFound
from django.http import Http404
from . import views 

handler404 = 'myapp.views.error_404'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('home/', views.home, name='home'),
    path('login_register/', views.login_register, name='login_register'),
    path('account/', views.my_account, name='my_account'),
    path('logout/', views.account_logout, name='logout'),
    path('shop/', views.shop, name='shop'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='wishlist_add'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='wishlist_remove'),
    path('cart/', views.cart, name='cart'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:product_id>/', views.product_detail, name='product')

]