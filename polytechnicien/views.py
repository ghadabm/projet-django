from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Bijoux, Textile
from django.http import HttpResponseNotFound
from django.contrib import messages

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('nom')
        price = request.POST.get('prix')
        description = request.POST.get('description')
        category = request.POST.get('categorie')
        image = request.FILES.get('image')
        
        # Create the appropriate product type based on category
        if category == 'textile':
            fabric_type = request.POST.get('fabric_type', 'Standard')
            product = Textile.objects.create(
                name=name,
                price=price,
                description=description,
                category=category,
                image=image,
                fabric_type=fabric_type
            )
        elif category == 'bijoux':
            material = request.POST.get('material', 'Standard')
            product = Bijoux.objects.create(
                name=name,
                price=price,
                description=description,
                category=category,
                image=image,
                material=material
            )
        
        messages.success(request, 'Produit ajouté avec succès!')
        return redirect('produits')
    return redirect('produits')

def update_product(request, product_id):
    if request.method == 'POST':
        # Get the product
        product = get_object_or_404(Product, id=product_id)
        
        # Update basic fields
        product.name = request.POST.get('nom')
        product.price = request.POST.get('prix')
        product.description = request.POST.get('description')
        
        # Check if category has changed
        new_category = request.POST.get('categorie')
        category_changed = product.category != new_category
        
        # Handle image update if provided
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        # If category changed, create new product of appropriate type
        if category_changed:
            # Create new product of appropriate type
            if new_category == 'textile':
                fabric_type = request.POST.get('fabric_type', 'Standard')
                new_product = Textile.objects.create(
                    name=product.name,
                    price=product.price,
                    description=product.description,
                    category=new_category,
                    image=product.image,
                    fabric_type=fabric_type
                )
            elif new_category == 'bijoux':
                material = request.POST.get('material', 'Standard')
                new_product = Bijoux.objects.create(
                    name=product.name,
                    price=product.price,
                    description=product.description,
                    category=new_category,
                    image=product.image,
                    material=material
                )
            
            # Delete old product
            product.delete()
        else:
            # Update existing product specific fields
            product.category = new_category
            product.save()
            
            if isinstance(product, Textile):
                product.fabric_type = request.POST.get('fabric_type', product.fabric_type)
                product.save()
            elif isinstance(product, Bijoux):
                product.material = request.POST.get('material', product.material)
                product.save()
                
        messages.success(request, 'Produit mis à jour avec succès!')
        return redirect('produits')
    
    return redirect('produits')


def product_list(request, category=None):
    search_query = request.GET.get('search', '')
    if category:
        produits = Product.objects.filter(category=category)
        selected_category = dict(Product.CATEGORY_CHOICES).get(category, "Tous les produits")
    else:
        produits = Product.objects.all()
        selected_category = "Tous les produits"
    
    # Apply search filter if provided
    if search_query:
        produits = produits.filter(name__icontains=search_query)
    
    # Check if products found after filtering
    if not produits:
        message = "Aucun produit trouvé"
    else:
        message = None
    
    return render(request, 'polytechnicien/produits.html', {
        'produits': produits,
        'selected_category': selected_category,
        'message': message,
    })

# This function is no longer needed since we're using home_view instead
# def homepage(request):
#    return render(request, 'polytechnicien/home.html')

def delete_product(request, id):
    try:
        # Try to find the product in any of the product models
        try:
            produit = Product.objects.get(id=id)
        except Product.DoesNotExist:
            try:
                produit = Bijoux.objects.get(id=id)
            except Bijoux.DoesNotExist:
                produit = Textile.objects.get(id=id)
        
        produit.delete()
        return redirect('produits')
    except:
        return HttpResponseNotFound("<h1>Produit introuvable</h1><a href='/produits/'>Retour</a>")

 

# This function is now the main home view
def home_view(request):
    produits = Product.objects.all()  # Fetch all products
    total_products = produits.count()  # Total number of products
    total_textiles = produits.filter(category='textile').count()  # Total textile products
    total_bijoux = produits.filter(category='bijoux').count()  # Total bijoux products

    # Prepare context with the products and statistics
    context = {
        'produits': produits,
        'total_products': total_products,
        'total_textiles': total_textiles,
        'total_bijoux': total_bijoux,
    }

    # Render the home.html page with the context data
    return render(request, 'polytechnicien/home.html', context)