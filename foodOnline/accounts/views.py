from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

#Restricting the vendor from accessing customer page
def check_role_vendor(user):               #passed inside decorator
    if user.role == 1:                     #gives the permission if logged in user is vendor
        return True
    else:
        raise PermissionDenied
    
# Restricting the customer from accessing vendor page
def check_role_customer(user):
    if user.role == 2:                     #gives the permission if logged in user is customer
        return True
    else:
        raise PermissionDenied   

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    
    elif request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # user = form.save(commit=False)      #The user is ready to be saved but not yet saved which means we can still alter it
            # password = form.cleaned_data['password']
            # user.set_password(password)         #We have hashed the password
            # user.role = User.CUSTOMER
            # user.save()

            #Hashing password using create_user from models
            #create user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            
            #send verification mail as the user has been registered
            send_verification_email(request, user)
            messages.success(request, 'Your account has been successfully registered')

            return redirect('registerUser')
        
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'YOu are already logged in!')
        return redirect('dashboard')
    
    if request.method=='POST':
        # store the data and create user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)     #We don't need to worry about vendor_name and vendor_license bcz 
        if form.is_valid() and v_form.is_valid():            #it is already there in request.POST and request.FILES
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            #send the verification mail to register the user
            send_verification_email(request, user)

            messages.success(request, 'Your account has been successfully registered! kindly wait for approval.')
            return redirect ('registerVendor') 
        else:
            print(form.errors)

    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form' : form,
        'v_form' : v_form
    }
    return render(request, 'accounts/registerVendor.html', context)

def activate(request, uidb64, token):
    #activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations !! Your Account is Activated')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    
    elif request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user:
            login_user(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('myAccount')
        
        else:
            messages.error(request, 'Invalid crediantials')
            return redirect('login')

        
    return render(request, 'accounts/login.html')

def logout(request):
    logout_user(request)
    messages.info(request, 'You are logged out')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):                   #function to take the customer and vendor to it's respective dashboard
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')