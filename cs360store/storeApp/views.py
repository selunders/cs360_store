from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.db.models import F
# Create your views here.
from django.contrib.auth.models import User

from storeApp.forms import ProductListingCreateForm, ServiceListingCreateForm
from .models import ShippingAddress, BillingAddress, ProductTag, ServiceTag, Vendor, Invoice, ProductListing, ServiceListing, InvoiceProduct, InvoiceService, CartProduct, CartService, Cart
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

@login_required
def MyCartListView(request):
    """View cart function for customer."""
    if request.user.cart:
        cart = request.user.cart
    else:
        cart = Cart(user=request.user)
        cart.save()

    cart_products = CartProduct.objects.filter(cart=cart)
    cart_services = CartService.objects.filter(cart=cart)

    context = {
        'cart_products': cart_products,
        'cart_services': cart_services,
    }
    
    return render(request, 'storeApp/customers/my_cart_detail.html', context)

@login_required
def CheckOutView(request):
    """View cart function for customer."""
    if request.user.cart:
        cart = request.user.cart
    else:
        cart = Cart(user=request.user)
        cart.save()

    cart_products = CartProduct.objects.filter(cart=cart)
    cart_services = CartService.objects.filter(cart=cart)

    context = {
        'cart_products': cart_products,
        'cart_services': cart_services,
    }
    
    return render(request, 'storeApp/customers/my_cart_detail.html', context)

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


class ServiceListingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'storeApp.can_set_active'
    template_name = 'storeApp/vendors/servicelisting_form.html'
    form_class = ServiceListingCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.vendor_id = self.request.user.vendor.id
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self, *args, **kwargs):
        initial = super(ServiceListingCreateView, self).get_initial(**kwargs)
        initial['name'] = 'Service Name'
        return initial
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ServiceListingCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs
    # success_url = reverse_lazy('manage-services')

class ProductListingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'storeApp.can_set_active'
    model = ProductListing
    fields = ['active', 'name','imageURL','price','description','quantity_available','restockDate','tags']
    template_name = 'storeApp/vendors/productlisting_form.html'
    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.vendor != self.request.user.vendor:
            raise Http404("You are not allowed to edit this product listing.")
        return super(ProductListingUpdateView, self).dispatch(request, *args, **kwargs)
    # success_url = reverse_lazy('index')

class ServiceListingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'storeApp.can_set_active'
    model = ServiceListing
    fields = ['active', 'name', 'imageURL', 'price', 'price_per_hour', 'description', 'service_area', 'days_available', 'tags']
    template_name = 'storeApp/vendors/servicelisting_form.html'
    def dispatch(self, request, *args, **kwargs):
        service = self.get_object()
        if service.vendor != self.request.user.vendor:
            raise Http404("You are not allowed to edit this service listing.")
        return super(ServiceListingUpdateView, self).dispatch(request, *args, **kwargs)
    # success_url = reverse_lazy('index')

@login_required
def MyCartAddProduct(request, pID, qty):
    """View cart function for customer."""
    success_url = reverse_lazy('my-cart')
    cart, exists = Cart.objects.get_or_create(user=request.user)
    q, exists = CartProduct.objects.get_or_create(cart=cart, product=ProductListing.objects.get(id=pID))
    q.quantity = F('quantity') + qty
    q.save()

    return HttpResponseRedirect(success_url)

@login_required
def MyCartAddService(request, sID):
    """View cart function for customer."""
    success_url = reverse_lazy('my-cart')
    cart, exists = Cart.objects.get_or_create(user=request.user)

    newCartService = CartService(cart=cart, service=ServiceListing.objects.get(id=sID))
    newCartService.save()
    
    return HttpResponseRedirect(success_url)