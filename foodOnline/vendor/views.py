from django.shortcuts import render
from django.http import HttpResponse 

def vprofile(request):
    return render(request, 'vendor/vprofile.html')