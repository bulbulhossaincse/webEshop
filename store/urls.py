from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import cart
from .import views
from .views import *

urlpatterns = [
    path('', views.Store, name='store'),
    path('search/', views.search, name="search"),
    path('<slug:category_slug>/',views.Store, name='products_by_category'), 
    path('<slug:category_slug>/<slug:product_slug>/',views.product_detail, name='product_detail'),  
    path('cart/', include('cart.urls')) 
    
]