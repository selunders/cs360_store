from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
from django.contrib.auth.models import User
from .models import ShippingAddress, BillingAddress, ProductTag, ServiceTag, Vendor, Invoice, ProductListing, ServiceListing, InvoiceProduct, InvoiceService
# ------------------
# Public Pages
# ------------------

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

class VendorListView(generic.ListView):
    model = Vendor

class VendorDetailView(generic.DetailView):
    model = Vendor

class ProductListView(generic.ListView):
    model = ProductListing

class ProductDetailView(generic.DetailView):
    model = ProductListing

class ServiceListView(generic.ListView):
    model = ServiceListing

class ServiceDetailView(generic.DetailView):
    model = ServiceListing

# ------------------
# Vendor Pages
# ------------------

class ManageProductsView(PermissionRequiredMixin, generic.ListView):
    """Generic view for managing a vendor's products."""
    model = ProductListing
    template_name = 'storeApp/vendors/manage_products.html'
    permission_required = 'storeApp.can_set_active'
    def get_queryset(self):
        return ProductListing.objects.filter(vendor=self.request.user.vendor)

class ManageServicesView(PermissionRequiredMixin, generic.ListView):
    """Generic view for managing a vendor's services."""
    model = ServiceListing
    template_name = 'storeApp/vendors/manage_services.html'
    permission_required = 'storeApp.can_set_active'
    def get_queryset(self):
        return ServiceListing.objects.filter(vendor=self.request.user.vendor)