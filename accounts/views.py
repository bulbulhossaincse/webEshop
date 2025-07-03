#from pyexpat.errors import messages
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from accounts.models import Account
from .forms import RegistrationForm

from django.views import generic
from django.urls import reverse_lazy
#from django.contrib import messages
#from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout

# varification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.core.mail import EmailMessage

from cart.views import _cart_id
from cart.models import CartItem, Cart

# Create your views here.
def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username,email=email).exists():
                messages.info(request, 'This username is already Exist')
                return redirect('register')
            else:
                user= User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password1)
                user.set_password(password1)
                user.is_staff=True
                user.is_active = False
                user.save()

                
                # user activation
                current_site = get_current_site(request)
                mail_subject = 'Please active your account'
                message = render_to_string('accounts/account_verification_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                # end activation


                #messages.success(request,'Thanks you for rester, please check your email that sent to your mail and click it.')
                return redirect('/accounts/login/?command=verification&email='+email)
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username, password=password)
         
        if user is not None:
            try:
                #print('entering inside try block')
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user=user
                        item.save()
            except:
                #print('entering inside except block')
                pass
            auth.login(request, user)
            messages.success(request, 'You are logged in!!!')
            return redirect('dashboard')
        else:
            messages.info(request, 'Invalid username or password!')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception as identifier:
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulation! Your account is activated.")
        return redirect('login')
    else:
        messages.error(request, "invalid activation link")
        return redirect('register')
    

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        #if User.objects.get(email=email).exists():
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            #reset password activation
            current_site = get_current_site(request)
            mail_subject = 'Please reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #message.success(request,'Password reset email has been to your email address')
            messages.success(request, "Please check your email to reset your password")
            return redirect('login')
            # end reset password activation
        else:
            #messages.error('Account does not exists.')
            messages.error(request, "Account does not exists.")
            return redirect('forgotPassword')
    return render(request,'accounts/forgotPassword.html')


def resetPassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception as identifier:
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('login')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset Successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')

    else:
        return render(request, 'accounts/resetPassword.html')
        
