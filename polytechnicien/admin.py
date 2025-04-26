from django import forms
from django.contrib import admin
from .models import Product, Textile, Bijoux

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']  # ✅ Ajout du champ image

    def save(self, commit=True):
        product = super().save(commit=False)
        if product.category == 'bijoux':
            Bijoux.objects.create(
                name=product.name,
                description=product.description,
                price=product.price,
                image=product.image,  # ✅ Ajouté ici
                material='Default Material'  # You can set this to be user-defined in a form
            )
        elif product.category == 'textile':
            Textile.objects.create(
                name=product.name,
                description=product.description,
                price=product.price,
                image=product.image,  # ✅ Ajouté ici
                fabric_type='Default Fabric'  # Again, you can make this user-defined
            )
        product.delete()  # After saving in the right category, delete the base product
        return product

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm

admin.site.register(Product, ProductAdmin)
admin.site.register(Textile)
admin.site.register(Bijoux)
