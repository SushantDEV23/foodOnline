from django.urls import path
from .views import *
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', vprofile, name='vprofile'),
    path('menu-builder/', menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', fooditems_by_category, name='fooditems_by_category')
]