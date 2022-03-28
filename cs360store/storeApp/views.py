from django.shortcuts import render

# Create your views here.
from .models import ShippingAddress, BillingAddress, ProductTag, ServiceTag, Vendor, Invoice, ProductListing, ServiceListing, InvoiceProduct, InvoiceService


def index(request):
    """View function for home page of the site."""

    num_vendors = Vendor.objects.all().count()
    num_sales = Invoice.objects.count()
    num_productsActive = ProductListing.objects.filter(active=True).count()
    num_servicesActive = ServiceListing.objects.filter(active=True).count()

    context = {
        'num_vendors': num_vendors,
        'num_sales': num_sales,
        'num_productsActive':  num_productsActive,
        'num_servicesActive': num_servicesActive,
    }

    return render(request, 'index.html', context = context)