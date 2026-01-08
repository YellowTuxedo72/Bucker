from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *

@login_required
def account(request):
    return render(request, 'myapp/account.html')


def about(request):
    return render(request, 'myapp/about.html', {'active': 'about'})

def faq(request):
    return render(request, 'myapp/faq.html', {'active': 'faq'})

def home(request):
    return render(request, 'myapp/index.html', {'active': 'home'})

def login_register(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                print("ну лол такого пользователя нет")
                error_message = 'Неправильный email или пароль'
            
        if 'register' in request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password1,
                        first_name=first_name,
                        last_name=last_name
                    )
                    login(request, user)
                    return redirect('home')
    return render(request, 'myapp/login-register.html')


@login_required
def my_account(request):
    return render(request, 'myapp/my-account.html')

def account_logout(request):
    logout(request)
    return redirect('login_register')

def shop(request):
    print(request.GET)
    sort = request.GET.get('sort_of_product_select', '1')
    print('SORT =', sort)

    products = Product.objects.all()

    if sort == '3':  # новинки
        products = products.order_by('-date_of_creation')
    elif sort == '4':  # дешёвые
        products = products.order_by('price')
    elif sort == '5':  # дорогие
        products = products.order_by('-price')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'myapp/shop.html', {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'total': paginator.count
    })

@login_required
def wishlist(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product')
    return render(request, 'myapp/wishlist.html', {
        'wishlist_items': items
    })

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    item = get_object_or_404(WishlistItem, user=request.user, product_id=product_id)
    item.delete()
    return redirect('wishlist')