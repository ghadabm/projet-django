from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('bijoux', 'Bijoux'),
        ('textile', 'Textile'),
    ]
    
    name = models.CharField(max_length=255)  # 'nom'
    description = models.TextField()  # 'description'
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 'prix'
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)  # 'categorie'
    image = models.ImageField(upload_to='product_images/')  # 'image' (ensure you have Pillow installed)
    
    def __str__(self):
        return self.name


class Textile(Product):
    fabric_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.fabric_type}"


class Bijoux(Product):
    material = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.material}"
