from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

