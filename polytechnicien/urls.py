# polytec_app/urls.py
# from django.contrib import admin
from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('home/')),
    
    path('home/', views.home_view, name='home'),
    
    path('produits/', views.product_list, name='produits'),
    path('propos/', views.propos, name='propos'),
    
    path('add-product/', views.add_product, name='add_product'),
    path('produit/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('produit/update/<int:id>/', views.update_product, name='update_product'),
    
    
    path('produits/<str:category>/', views.product_list, name='product_list_by_category'),
]