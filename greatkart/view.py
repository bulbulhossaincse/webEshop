from urllib import request
from django.shortcuts import render,redirect
from django.views import generic
from django.core import paginator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.utils.text import slugify
from store.models import ( Banners,Product)
from store.views import Store

def home(request):
     products= Product.objects.all().filter(is_available=True).order_by('id')
     paginator = Paginator(products, 6)
     page = request.GET.get('page')
     page_products = paginator.get_page(page)
     product_count= products.count()
     banner=Banners.objects.all()
     context={
          'products':page_products,
          'product_count':product_count,
          'banner':banner,
     }
     return render(request,'index.html',context)