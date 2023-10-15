from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse 
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from  django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.views import check_role_vendor
from menu.models import *
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify

def get_vendor(request):                      # Call this function when getting vendor object
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method=='POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)  #request.FILES is for the picture to upload
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings saved .')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile':profile,
        'vendor' : vendor,
    }
    return render(request, 'vendor/vprofile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories':categories
    }
    return render(request, 'vendor/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'fooditems':fooditems,
        'category':category
    }
    return render(request, 'vendor/fooditems_by_category.html', context)



#Below code for Add Category CRUD
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category Added Successfuly!! ')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
        'form':form,
    }
    return render(request, 'vendor/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category Updated Successfuly!! ')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category':category
    }
    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category Deleted Successfuly!! ')
    return redirect('menu_builder')


# Below code Add food CRUD
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request, 'Food Item Added Successfuly!! ')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
    context = {
        'form':form,
    }

    return render(request, 'vendor/add_food.html', context)

def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request, 'Food Item Updated Successfuly!! ')
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food)
    context = {
        'form':form,
        'food':food
    }
    return render(request, 'vendor/edit_food.html', context)

def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages = 'Food Item has been deleted Successfully'
    return redirect('fooditems_by_category', food.category.id)
