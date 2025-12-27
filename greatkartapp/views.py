from django.shortcuts import get_object_or_404, render

from greatkartapp.models import Category, Product

# Create your views here.

def index(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(request, 'greatkartapp/index.html', context)

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug:
        # For URL: /store/shirt/ (or /category/shirt/ depending on your pattern)
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        # For URL: /store/
        products = Product.objects.filter(is_available=True)
        product_count = products.count()
    
    # Common context (move outside if/else)
    context = {
        'products': products,
        'product_count': product_count,
        #'current_category': categories,  # Will be None for /store/
    }
    
    return render(request, 'greatkartapp/store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    context ={
        'single_product': single_product,
    }
        
    return render(request, 'greatkartapp/store/product_detail.html', context) 

def cart(request):
    return render(request, 'greatkartapp/store/cart.html')  