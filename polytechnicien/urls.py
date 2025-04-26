# polytec_app/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views
from django.shortcuts import redirect

urlpatterns = [
    # Root redirects to home
    path('', lambda request: redirect('home/')),
    
    # Main pages
    path('home/', views.home_view, name='home'),
    
    # Single consistent name for product list
    path('produits/', views.product_list, name='produits'),
    
    # Product CRUD operations
    path('add-product/', views.add_product, name='add_product'),
    path('produit/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('produit/update/<int:id>/', views.update_product, name='update_product'),
    
    # Category filtering
    path('produits/<str:category>/', views.product_list, name='product_list_by_category'),
]