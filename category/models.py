from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photes/categories', blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
        #ordering=['category_name']  
    def __str__(self) -> str:
        return self.category_name
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

   

