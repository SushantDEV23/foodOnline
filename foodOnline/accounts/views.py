from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages

def registerUser(request):
    if request.method=='POST':
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