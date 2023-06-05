from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User

def registerUser(request):
    if request.method=='POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)      #The user is ready to be saved but not yet saved which means we can still alter it
            user.role = User.CUSTOMER
            user.save()
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/registerUser.html', context)