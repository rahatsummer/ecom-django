from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cart, CartItem, Product, Category
from django.core.exceptions import ObjectDoesNotExist
from greatkartapp.models import Category, Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def index(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(request, 'greatkartapp/index.html', context)

# views.py



def store(request, category_slug=None):
    categories = None
    products = None
    paged_products = None
    product_count = 0

    if category_slug:
        # For URL: /store/shirt/ (or /category/shirt/ depending on your pattern)
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)       
        product_count = products.count()

        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        # For URL: /store/
        products = Product.objects.filter(is_available=True)
        product_count = products.count()  # Count on QuerySet
         # Apply pagination
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    
    # Common context (move outside if/else)
    context = {
         'products': paged_products,  # Use paginated results
        'product_count': product_count,
        'categories': categories,  # Will be None for /store/
        #'current_category': categories,  # Will be None for /store/
    }
    
    return render(request, 'greatkartapp/store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        #return HttpResponse(in_cart)
        #exit()
    except Exception as e:
        raise e
    
    context ={
        'single_product': single_product,
        'in_cart': in_cart,
    }
        
    return render(request, 'greatkartapp/store/product_detail.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart 

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    # Logic to add the product to the cart goes here   
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity=1)
    #return HttpResponse(cart_item.product)
    #exit()
    return redirect('cart')

def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
    except:
        pass
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass # just ignore

    context = { 'total': total, 
               'quantity': quantity, 
               'cart_items': cart_items,
                'tax': tax,
                'grand_total': grand_total,}
    return render(request, 'greatkartapp/store/cart.html', context)  


