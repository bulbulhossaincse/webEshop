#from django.contrib import admin
from django.urls import path
#from django.conf import settings
#from django.conf.urls.static import static
#from .views import *
from .import views

urlpatterns = [ 
   path('register/',views.register, name='register'),
   path('login/',views.login, name='login'),
   path('logout/',views.logout, name='logout'),
   path('dashboard/',views.dashboard, name='dashboard'),
   path('',views.dashboard, name='dashboard'), 

   path('activate/<uidb64>/<token>/', views.activate, name='activate'),
   path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
   path('resetPassword_validate/<uidb64>/<token>/', views.resetPassword_validate, name='resetPassword_validate'),
   path('resetPassword/',views.resetPassword,name='resetPassword'),
]