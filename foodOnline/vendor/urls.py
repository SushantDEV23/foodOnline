from django.urls import path
from .views import *
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', vprofile, name='vprofile'),
]