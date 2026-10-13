from django.shortcuts import render, redirect, get_object_or_get_404
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm

# Create your views here.
def category(request,foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("Sorry, That Category Doesn't Exist"))
        return redirect('home')

def product(request,pk):
    product = get_object_or_get_404(Product, pk=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all() 
    return render(request, 'home.html', {'products':products})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,"Welcome Back!")
            return redirect('home')
        else:
            messages.error(request,("Ooops! That's Not Right, Please Try Again"))
            return render(request, 'login.html', {'username': username})
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,("You have logged out! We Hope You Enjoyed Your Session!"))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() 
            
            # Use Django's authenticate framework safely on the saved object
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You Have Successfully Signed Up!")
                return redirect('home')
        else:
            messages.error(request, "Ooops! An error occurred while registering.")
    else:
        form = SignUpForm()
        
    return render(request, 'register.html', {'form': form})

