from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *

def about(request):
    return render(request, 'myapp/about.html', {'active': 'about'})

def faq(request):
    return render(request, 'myapp/faq.html', {'active': 'faq'})

def home(request):
    products = Product.objects.order_by('-date_of_creation')[:8]
    return render(request, 'myapp/index.html', {'active': 'home', 'products':products})

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
                print("ура вы успешно зашли")
                return redirect('home')
            else:
                print("Ну такого пользователя нет(()()())")

            
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
    orders = Order.objects.filter(user=request.user).order_by('-date_of_creation')
    return render(request, 'myapp/my-account.html', {'orders': orders})

def account_logout(request):
    logout(request)
    return redirect('login_register')

def shop(request):
    print(request.GET)
    sort = request.GET.get('sort_of_product_select', '1')
    print('SORT =', sort)

    products = Product.objects.all()

    if sort == '3': 
        products = products.order_by('-date_of_creation')
    elif sort == '4':
        products = products.order_by('price')
    elif sort == '5':
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
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_from_wishlist(request, product_id):
    item = get_object_or_404(WishlistItem, user=request.user, product_id=product_id)
    item.delete()
    return redirect('wishlist')

@login_required
def cart(request):
    cart = get_or_create_cart(request.user)
    items = cart.cart_detatils.select_related('product')

    if request.method == 'POST' and 'update_cart' in request.POST:
        for item in items:
            key = f'quantity_{item.id}'
            if key in request.POST:
                item.quantity = int(request.POST[key])
                item.save()
        return redirect('cart')

    total = sum(item.total_price for item in items)
    return render(request, 'myapp/cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request.user)

    item, created = CartDetails.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1

    item.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def cart_remove(request, item_id):
    item = get_object_or_404(CartDetails, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

def checkout(request):
    return render(request, 'myapp/checkout.html')

@login_required
def checkout(request):
    cart = get_or_create_cart(request.user)
    products_from_cart = cart.cart_detatils.select_related('product')
    total_sum = sum(product.total_price for product in products_from_cart)
    user = request.user
    if request.method == 'POST':
        order = Order.objects.create(
            user=user,
            status=Order.Status.PROCESSING,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            address=request.POST['address'],
            city=request.POST['city'],
            country=request.POST['country'],
            postcode=request.POST['postcode'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            total_price=total_sum
        )

        for product_from_cart in products_from_cart:
            OrderDetails.objects.create(
                order=order,
                product=product_from_cart.product,
                price=product_from_cart.product.price,
                quantity=product_from_cart.quantity
            )

        products_from_cart.delete()
        return redirect('home')

    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    return render(request, 'myapp/checkout.html', {
        'products': products_from_cart,
        'total': total_sum,
        'data': data
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'myapp/single-product.html', {'product': product})









def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart