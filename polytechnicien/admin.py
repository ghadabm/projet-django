from django import forms
from django.contrib import admin
from .models import Product, Textile, Bijoux

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']  

    def save(self, commit=True):
        product = super().save(commit=False)
        if product.category == 'bijoux':
            Bijoux.objects.create(
                name=product.name,
                description=product.description,
                price=product.price,
                image=product.image, 
                material='Default Material' 
            )
        elif product.category == 'textile':
            Textile.objects.create(
                name=product.name,
                description=product.description,
                price=product.price,
                image=product.image,  
                fabric_type='Default Fabric'  
            )
        product.delete()  
        return product

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm

admin.site.register(Product, ProductAdmin)
admin.site.register(Textile)
admin.site.register(Bijoux)
