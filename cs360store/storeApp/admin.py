from dataclasses import fields
from django.contrib import admin

# Register your models here.

from .models import ShippingAddress, BillingAddress, Vendor, Invoice, ProductListing, ServiceListing, InvoiceProduct, InvoiceService, ProductTag, ServiceTag, Cart

# ------------------
# ---- Inlines ----- 
# ------------------
class Inline_ShippingAddress(admin.TabularInline):
    model = ShippingAddress
    extra = 1


class Inline_InvoiceProduct(admin.StackedInline):
    model = InvoiceProduct
    fieldsets = [(None, {'fields': ('product', 'vendor', 'unit_price', 'quantity_ordered', 'status')})]
    readonly_fields = ['vendor', 'unit_price']
    # readonly_fields = ['vendor_name', 'product']
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        if obj: #This is the case when obj is already created i.e. it's an edit
            return ['vendor', 'unit_price','product', 'quantity_ordered']
        else:
            return ['vendor', 'unit_price']    

class Inline_InvoiceService(admin.StackedInline):
    model = InvoiceService
    fieldsets = [(None, {'fields': ('service', 'vendor', 'price_paid', 'status')})]
    
    # readonly_fields = ['vendor_name', 'service']
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        if obj: #This is the case when obj is already created i.e. it's an edit
            return ['vendor', 'price_paid', 'service']
        else:
            return ['vendor',]

# class Inline_ProductListing(admin.TabularInline):
class Inline_ProductListing(admin.StackedInline):
    model = ProductListing
    list_display = ('name', 'list_tags', 'vendor', 'price', 'quantity_available', 'active')
    inlines = [Inline_InvoiceProduct]
    extra = 0

# class Inline_ServiceListing(admin.TabularInline):
class Inline_ServiceListing(admin.StackedInline):
    model = ServiceListing
    readonly_fields = ['vendor',]
    extra = 0


class Inline_Invoice(admin.TabularInline):
    model = Invoice
    show_change_link = True
    readonly_fields = ['total_payment',]
    extra = 0

# class Inline_ProductTag(admin.TabularInline):
#     model = ProductTag
#     extra = 1

# class Inline_ServiceTag(admin.TabularInline):
#     model = ServiceTag
#     extra = 1
# -----------------

class BillingAddress(admin.TabularInline):
    model = BillingAddress
    extra = 1

class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'owner', 'date_created')
    fieldsets = [
        (None, 
        {
            'fields':('vendor_name', 'owner', 'date_created')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'emergency_phone_number'),
        }),
        ('Address Info', {
            'fields': ('address1', 'address2', 'zip_code', 'city', 'state_or_province', 'country'),
        }),
    ]
    search_fields = ['vendor_name']

    inlines = [Inline_ProductListing, Inline_ServiceListing]

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchaser', 'date_placed', 'total_payment')
    list_filter = ('date_placed',)
    inlines = [Inline_InvoiceProduct, Inline_InvoiceService]
    search_fields = ['id']

class ProductListingAdmin(admin.ModelAdmin):
    list_filter = ('active','vendor', )
    list_display = ('name', 'list_tags', 'vendor', 'price', 'quantity_available', 'active')
    def get_readonly_fields(self, request, obj=None):
        if obj: #This is the case when obj is already created i.e. it's an edit
            return ['vendor',]
        else:
            return []

class ServiceListingAdmin(admin.ModelAdmin):
    list_filter = ('active', 'vendor')
    list_display = ('name', 'list_tags', 'vendor', 'price', 'days_available', 'active')
    def get_readonly_fields(self, request, obj=None):
        if obj: #This is the case when obj is already created i.e. it's an edit
            return ['vendor',]
        else:
            return []

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'subtotal')

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Invoice, InvoiceAdmin)
# admin.site.register(InvoiceProduct)
# admin.site.register(InvoiceService)
admin.site.register(ProductListing, ProductListingAdmin)
admin.site.register(ServiceListing, ServiceListingAdmin)
admin.site.register(ProductTag)
admin.site.register(ServiceTag)
admin.site.register(Cart, CartAdmin)