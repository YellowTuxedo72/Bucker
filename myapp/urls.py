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
    path('logout/', views.account_logout, name='logout')
]