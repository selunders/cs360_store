from django.contrib import admin

# Register your models here.

from .models import ShippingAddress, BillingAddress, Vendor, Invoice, ProductListing, ServiceListing, InvoiceProduct, InvoiceService, ProductTag, ServiceTag

# ------------------
# ---- Inlines ----- 
# ------------------
class Inline_ShippingAddress(admin.TabularInline):
    model = ShippingAddress
    extra = 1


# class Inline_ProductListing(admin.TabularInline):
class Inline_ProductListing(admin.StackedInline):
    model = ProductListing
    extra = 0

# class Inline_ServiceListing(admin.TabularInline):
class Inline_ServiceListing(admin.StackedInline):
    model = ServiceListing
    extra = 0

class Inline_InvoiceProduct(admin.StackedInline):
    model = InvoiceProduct
    extra = 0

class Inline_InvoiceService(admin.StackedInline):
    model = InvoiceService
    extra = 0

class Inline_Invoice(admin.TabularInline):
    model = Invoice
    show_change_link = True
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

    inlines = [Inline_Invoice, Inline_ProductListing, Inline_ServiceListing]

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'id', 'date_placed')
    list_filter = ('vendor', 'date_placed')
    inlines = [Inline_InvoiceProduct, Inline_InvoiceService]

class ProductListingAdmin(admin.ModelAdmin):
    list_filter = ('active','vendor', )
    list_display = ('name', 'list_tags', 'vendor', 'price', 'quantity_available', 'active')

class ServiceListingAdmin(admin.ModelAdmin):
    list_filter = ('active', 'vendor')
    list_display = ('name', 'list_tags', 'vendor', 'price', 'days_available', 'active')

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Invoice, InvoiceAdmin)
# admin.site.register(InvoiceProduct)
# admin.site.register(InvoiceService)
admin.site.register(ProductListing, ProductListingAdmin)
admin.site.register(ServiceListing, ServiceListingAdmin)
admin.site.register(ProductTag)
admin.site.register(ServiceTag)