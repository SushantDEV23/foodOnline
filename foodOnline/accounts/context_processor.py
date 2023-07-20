from vendor.models import Vendor

def get_vendor(request):            #with the help of this user data will be available to all the templates
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)