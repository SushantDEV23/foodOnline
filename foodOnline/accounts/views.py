from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User
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