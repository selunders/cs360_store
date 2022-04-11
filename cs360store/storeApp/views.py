from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.urls import reverse, reverse_lazy
from django.db.models import F
# Create your views here.
from django.contrib.auth.models import User

from storeApp.forms import CartProductUpdateForm, ProductListingCreateForm, ServiceListingCreateForm, CartProductForm
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

class ProductDetailView(generic.DetailView, FormMixin):
    model = ProductListing
    form_class = CartProductForm
    def get_initial(self):
        return {
            'product': self.get_object(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartProductForm(initial={'qty':1})
        return context

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

class ManageProductOrdersView(PermissionRequiredMixin, generic.ListView):
    """Generic view for managing a vendor's sold products."""
    model = InvoiceProduct
    template_name = 'storeApp/vendors/manage_product_orders.html'
    permission_required = 'storeApp.can_set_active'
    def get_queryset(self):
        return InvoiceProduct.objects.filter(vendor=self.request.user.vendor)

class ManageServiceOrdersView(PermissionRequiredMixin, generic.ListView):
    """Generic view for managing a vendor's sold products."""
    model = InvoiceService
    template_name = 'storeApp/vendors/manage_service_orders.html'
    permission_required = 'storeApp.can_set_active'
    def get_queryset(self):
        return InvoiceService.objects.filter(vendor=self.request.user.vendor)

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
def MyCartAddProduct(request, pID):
    """View cart function for customer."""
    success_url = reverse_lazy('my-cart')
    cart, exists= Cart.objects.get_or_create(user=request.user)

    if request.method=='POST':
        form=CartProductForm(request.POST)
        if form.is_valid():
            cp, exists = cart.cartproduct_set.get_or_create(cart=cart, product=ProductListing.objects.get(id=pID))
            cp.quantity = cp.quantity + form.cleaned_data['qty']# possible race condition, can't see this one being an issue
            if cp.quantity > 9999:
                cp.quantity = 9999
            cp.save()
    return HttpResponseRedirect(success_url)

@login_required
def MyCartAddService(request, csID):
    """View to add a product to cart"""
    success_url = reverse_lazy('my-cart')
    cart, exists= Cart.objects.get_or_create(user=request.user)
    if request.method=='POST':
            cs, exists = cart.cartservice_set.get_or_create(cart=cart, service=ServiceListing.objects.get(id=csID))
            if not exists:
                cs.save()
    return HttpResponseRedirect(success_url)

@login_required
def MyCartRemoveProduct(request, pID):
    """View cart function for customer."""
    success_url = reverse_lazy('my-cart')
    cart, exists= Cart.objects.get_or_create(user=request.user)

    if request.method=='POST':
        form=CartProductForm(request.POST)
        if form.is_valid():
            cp, exists = cart.cartproduct_set.get_or_create(cart=cart, product=ProductListing.objects.get(id=pID))
            cp.quantity = form.cleaned_data['qty']# possible race condition, can't see this one being an issue
            if cp.quantity > 9999:
                cp.quantity = 9999
            elif cp.quantity < 0:
                cp.quantity = 0
            cp.save()
    return HttpResponseRedirect(success_url)

@login_required
def MyCartRemoveService(request, csID):
    """View cart function for customer."""
    cart, exists= Cart.objects.get_or_create(user=request.user)
    if request.method=='POST':
            cs = cart.cartservice_set.get(service=ServiceListing.objects.get(id=csID))
            cs.delete()
    return HttpResponseRedirect(reverse('my-cart'))

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
    cart_subtotal = cart.get_subtotal()

    context = {
        'cart_products': cart_products,
        'cart_services': cart_services,
        'subtotal': cart_subtotal,
        'cproduct_remove_form': CartProductUpdateForm(),
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
    cart_subtotal = cart.get_subtotal()

    if cart_products.exists() or cart_services.exists():
        newInvoice = Invoice(purchaser = request.user, total_payment = cart_subtotal)
        newInvoice.save()

    if cart_products.exists():
        for cproduct in cart_products:
            newInvoiceProduct = InvoiceProduct(invoice = newInvoice, product = cproduct.product, unit_price = cproduct.product.price, quantity_ordered = cproduct.quantity)
            newInvoiceProduct.save()
            cproduct.delete()
    
    if cart_services.exists():
        for cservice in cart_services:
            newInvoiceService = InvoiceService(invoice = newInvoice, service = cservice.service, price_paid = cservice.service.price)
            newInvoiceService.save()
            cservice.delete()

    return HttpResponseRedirect(reverse('my-orders'))