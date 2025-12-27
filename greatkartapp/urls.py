from django.urls import path
from greatkartapp import views

urlpatterns = [
    path('index/', views.index, name='index'),

    # Single pattern that handles both
    path('store/', views.store, name='store'),  # /store/
    path('store/<slug:category_slug>/', views.store, name='products_by_category'),  # /store/shirt/
    path('store/category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),

    #Cart URLs
    path('cart/', views.cart, name='cart'),
]
