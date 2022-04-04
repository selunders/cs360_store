from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

# Create your views here.
from django.contrib.auth.models import User

from storeApp.forms import ProductListingCreateForm
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
# Customer Pages
# ------------------
class MyOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Invoice
    template_name = 'storeApp/customers/my_orders_list.html'
    def get_queryset(self):
        return Invoice.objects.filter(purchaser=self.request.user)

class MyOrdersDetailView(LoginRequiredMixin, generic.DetailView):
    model = Invoice
    template_name = 'storeApp/customers/my_orders_detail.html'

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

    # path('manage-products/create', views.ProductListingCreateView.as_view(), name='create-product'),
    # path('manage-services/create', views.ServiceListingCreateView.as_view(), name='create-product'),
    # path('manage-products/<uuid:pk>/update', views.ProductListingCreateView.as_view(), name='update-product'),
    # path('manage-services/<uuid:pk>/update', views.ServiceListingCreateView.as_view(), name='update-service'),

class ProductListingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'storeApp.can_set_active'
    template_name = 'storeApp/vendors/productlisting_form.html'
    form_class = ProductListingCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.vendor_id = self.request.user.vendor.id
        self.object.tags
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self, *args, **kwargs):
        initial = super(ProductListingCreateView, self).get_initial(**kwargs)
        initial['name'] = 'Product Name'
        return initial
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProductListingCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    # success_url = reverse_lazy('manage-products')

# class BookCreateView(CreateView):
    # template_name = 'books/book-create.html'
    # form_class = BookCreateForm
# 
    # def form_valid(self, form):
        # self.object = form.save(commit=False)
        # self.object.user = self.request.user
        # self.object.save()
        # return HttpResponseRedirect(self.get_success_url())
# 
    # def get_initial(self, *args, **kwargs):
        # initial = super(BookCreateView, self).get_initial(**kwargs)
        # initial['title'] = 'My Title'
        # return initial
# 
    # def get_form_kwargs(self, *args, **kwargs):
        # kwargs = super(BookCreateView, self).get_form_kwargs(*args, **kwargs)
        # kwargs['user'] = self.request.user
        # return kwargs