from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category,  Order, OrderItem
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from django.db.models import Q

# Create your views here.
def category(request,foo):
    clean_category_name = foo.replace('-', ' ')
    try:
        category_obj = Category.objects.get(name__iexact=clean_category_name)
        products = Product.objects.filter(category=category_obj)
        return render(request, 'category.html', {'products':products, 'category':category_obj})
    except Category.DoesNotExist:
        messages.error(request, ("Sorry, That Category Doesn't Exist"))
        return redirect('home')

def product(request,pk):
    product = get_object_or_404(Product, pk=pk)
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

### Adding in product search
def search(request):
    ### Get the string from the browser search
    query = request.GET.get('q') 
    products = Product.objects.none()
    
    if query:
        ### Filter by names or description of product
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
    return render(request, 'search.html', {'products': products, 'query': query})


### Transaction engine
def checkout(request):
    """Creates the simulated order collection form."""
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    
    ### Stop if cart is empty
    if len(cart) == 0:
        messages.error(request, "Your cart is empty! Add some party essentials first.")
        return redirect('home')
        
    return render(request, "checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals
    })

### Process the order 
def process_order(request):
    """Processes mock checkout validation and saves logs"""
    if request.method == "POST":
        cart = Cart(request)
        totals = cart.cart_total()
        
        ### Get details from POST payload map
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        shipping_address = request.POST.get('shipping_address')
        
        ### Make sure info is fully filled out 
        if not full_name or not email or not shipping_address:
            messages.error(request, "Please fill out all billing and shipping completely.")
            return redirect('checkout')
            
        ### Creating and saving a new order record in the database
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            shipping_address=shipping_address,
            amount_paid=totals,
            status="Demo - Not Paid" ### Not a real store so important to let them know they're not spending money
        )
        
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        
        for product in cart_products:
            ### Checks if its on sale. If it is, it uses the sale price otherwise using normal price
            current_price = product.sale_price if product.is_sale else product.price
            qty = quantities.get(str(product.id))
            
            ### Makes a snapshot of the object for receipts
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                price=current_price,
                quantity=qty
            )
            
            ### When bought the stock should go down
            if hasattr(product, 'stock'):
                product.stock -= int(qty)
                product.save()

        ### Wiping the session after the order goes through
        request.session['session_key'] = {}
        request.session.modified = True
        
        messages.success(request, f"Demo Order #{order.id} saved! No real payment was processed.")
        return render(request, "order_confirmation.html", {"order": order})
        
    return redirect('home')



@login_required(login_url='login')
def order_history(request):
    """Gets all previous demo purchases belonging to the  user."""
    ### Make sure users can only see their orders
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    
    return render(request, 'order_history.html', {'orders': orders})

