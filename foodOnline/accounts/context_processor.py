from vendor.models import Vendor
from django.conf import settings

def get_vendor(request):            #with the help of this user data will be available to all the templates
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)

def get_google_api(request):
    return {'HERE_API_KEY' : settings.HERE_API_KEY}