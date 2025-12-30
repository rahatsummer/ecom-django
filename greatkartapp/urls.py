from django.urls import path
from greatkartapp import views

urlpatterns = [
    path('index/', views.index, name='index'),

    # Single pattern that handles both
    path('store/', views.store, name='store'),  # /store/
    path('store/category/<slug:category_slug>/', views.store, name='products_by_category'),  # /store/shirt/
    path('store/category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),

    path('search/', views.search, name='search'),

    #Cart URLs
    path('cart/', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
]
