from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from category.models import Category


# Create your models here.
class Banners(models.Model):
    title = models.CharField(max_length=100,unique=True)
    banner_image= models.ImageField(upload_to='photes/banners')
    created_date=models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.title 
    
class Product(models.Model):
    category=models.ForeignKey(Category,related_name='products', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.IntegerField()
    images= models.ImageField(upload_to='photes/products')
    stock = models.IntegerField()
    is_available= models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modify_date=models.DateTimeField(auto_now=True)
    
    


    def __str__(self) -> str:
        return self.product_name
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    objects = VariationManager()

    def __str__(self):
        return self.variation_value