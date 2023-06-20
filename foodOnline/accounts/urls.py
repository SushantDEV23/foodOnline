from django.urls import path
from .views import *
urlpatterns = [
    path('registerUser/', registerUser, name='registerUser'),
    path('registerVendor/', registerVendor, name='registerVendor'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('myAccount/', myAccount, name='myAccount'),
    path('customerDashboard', customerDashboard, name='customerDashboard'),
    path('vendorDashboard', vendorDashboard, name='vendorDashboard')
]
