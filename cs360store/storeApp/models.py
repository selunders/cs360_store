from ast import Delete
from email.policy import default
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse # generate URLS by reversing URL patterns
import uuid # for unique instances
from django.db.models import F # for better database access
from django.core.validators import MaxValueValidator

# Create your models here.

class ShippingAddress(models.Model):
    """Model representing a shipping address."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024, help_text="Enter your full name.")
    address1 = models.CharField(max_length=1024, help_text="Address line 1")
    address2 = models.CharField(max_length=1024, help_text="Address line 2")
    zip_code = models.CharField(max_length=12, help_text="Zip Code")
    city = models.CharField(max_length=1024, help_text="City")
    country = models.CharField(max_length=1024, help_text="Country")

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

class BillingAddress(models.Model):
    """Model representing a shipping address."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024, help_text="Enter your full name.")
    address1 = models.CharField(max_length=1024, help_text="Address line 1")
    address2 = models.CharField(max_length=1024, help_text="Address line 2")
    zip_code = models.CharField(max_length=12, help_text="Zip Code")
    city = models.CharField(max_length=1024, help_text="City")
    country = models.CharField(max_length=1024, help_text="Country")

    class Meta:
        verbose_name = "Billing Address"
        verbose_name_plural = "Billing Addresses"


class ProductTag(models.Model):
    """Model representing a tag for a product."""
    name = models.CharField(max_length=200, help_text="Enter a tag; i.e. \"electronics\"", primary_key=True, unique=True)
    # product = models.ManyToManyField(ProductListing, blank=True)
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(ProductTag, self).save(*args, **kwargs)

class ServiceTag(models.Model):
    """Model representing a tag for a service."""
    name = models.CharField(max_length=200, help_text="Enter a tag; i.e. \"electronics\"", primary_key=True, unique=True)
    # service = models.ManyToManyField(ServiceListing, blank=True)
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(ServiceTag, self).save(*args, **kwargs)
# class BillingAddress(ShippingAddress):
    # tax_number = models.IntegerField(max_length=10, help_text="Tax Number")


class Vendor(models.Model):
    """Model representing a unique vendor."""
    vendor_name = models.CharField(max_length=200, help_text="Enter your vendor name.", unique=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=20, help_text="1 (234) 567 8901")
    emergency_phone_number = models.CharField(max_length=20, help_text="1 (234) 567 8901")

    # full_address = models.CharField(max_length=1024, help_text="Enter your full address.")
    address1 = models.CharField(max_length=1024, help_text="Address line 1")
    address2 = models.CharField(max_length=1024, help_text="Address line 2", null=True, blank=True)
    zip_code = models.CharField(max_length=12, help_text="Zip Code")
    city = models.CharField(max_length=1024, help_text="City")
    state_or_province = models.CharField(max_length=1024, help_text="State/Province (if applicable)", null=True, blank=True)
    country = models.CharField(max_length=1024, help_text="Country")

    date_created = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.vendor_name

    def get_absolute_url(self):
        """Returns the url to access this vendor's page."""
        return reverse('vendor-detail', args=[str(self.id)])

class Invoice(models.Model):
    """Model representing an invoice for an order"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular order", editable=False)
    purchaser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_placed = models.DateTimeField(default=datetime.now, blank=True)
    # payment_amount = models.DecimalField(decimal_places=2, max_digits=9)
    total_payment = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        """Returns the url to access this order's page."""
        return reverse('my-orders-detail', args=[str(self.id)])
    # @property
    # def total_payment(self):
        # """Return sum of payments for attached products/services."""
        # return float(InvoiceProduct.objects.filter(invoice__exact=self.id).aggregate(total_payment=models.Sum(F('unit_price') * F('quantity_ordered'))).get('total_payment') or 0) \
            # + float(InvoiceService.objects.filter(invoice__exact=self.id).aggregate(total_payment=models.Sum(F('price_paid'))).get('total_payment') or 0)
    
    def save(self, *args, **kwargs):
        self.total_payment = float(InvoiceProduct.objects.filter(invoice__exact=self.id).aggregate(total_payment=models.Sum(F('unit_price') * F('quantity_ordered'))).get('total_payment') or 0) \
            + float(InvoiceService.objects.filter(invoice__exact=self.id).aggregate(total_payment=models.Sum(F('price_paid'))).get('total_payment') or 0)
        super(Invoice, self).save(*args, **kwargs)
    # @property
    # def total_payment(self):
    #     """Return sum of payments for attached products/services."""
    #     return self.total_products + self.total_services

class ProductListing(models.Model):
    """Model representing a product for sale."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular order", editable=False)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=200, help_text="Enter a name for your product.")
    imageURL = models.URLField(max_length=200, help_text="Enter image URL", default="https://picsum.photos/400/300")
    # price = models.DecimalField(max_digits=7, decimal_places=2) # allows max price of $99,999.99
    price = models.DecimalField(decimal_places=2, max_digits=7) # allows max price of $99,999.99
    description = models.TextField()
    quantity_available = models.IntegerField(help_text="How many are available? Leave blank if unlimited.", null=True, blank=True)
    restockDate = models.DateField(help_text="Leave blank if N/A",null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT)
    tags = models.ManyToManyField(ProductTag, blank=True)
    # options = models.CharField()

    def setActive(self, state):
        self.active = state
    
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        """Returns the url to access details for this product."""
        return reverse('product-detail', args=[str(self.id)])

    def list_tags(self):
        return ', '.join(tag.name for tag in self.tags.all()[:3])

    list_tags.short_description = 'Tags'
    class Meta:
        permissions = (("can_set_active", "Set product as active"),)

class ServiceListing(models.Model):
    """Model representing a service being offered."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular service", editable=False)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=200, help_text="Enter a name for your service.")
    imageURL = models.URLField(max_length=200, help_text="Enter image URL", blank="True", null=True, default="https://picsum.photos/400/300")
    price = models.DecimalField(help_text="Max: 99,999.99. Set 0 \'Free\'", max_digits=7, decimal_places=2) # allows max price of $99,999.99
    price_per_hour = models.BooleanField(help_text="Is this service priced per hour?", default=False)
    description = models.TextField()
    service_area = models.IntegerField(help_text="Enter miles from your Business Address that you service.")
    days_available = models.CharField(max_length=200, help_text="Enter the days/times this service is available, i.e. M-Th 9-5, Fri-Sun 10-1", null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT)
    tags = models.ManyToManyField(ServiceTag, blank=True)
    # options = models.CharField()

    def setActive(self, state):
        self.active = state
    
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        """Returns the url to access details for this service."""
        return reverse('service-detail', args=[str(self.id)])

    def list_tags(self):
        return ', '.join(tag.name for tag in self.tags.all()[:3])

    list_tags.short_description = 'Tags'

class InvoiceProduct(models.Model):
    """Model representing a product in an order."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular service", editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,)
    product = models.ForeignKey(ProductListing, on_delete=models.RESTRICT)
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT, blank=True)
    unit_price = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    quantity_ordered = models.IntegerField(default=1, validators=[MaxValueValidator(9999)])
    # total_payment = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    ORDER_STATUS = (
        ('or', 'Order Received'),
        ('cl', 'Canceled'),
        ('sh', 'Shipped'),
    )
    status = models.CharField(
        max_length=2,
        choices=ORDER_STATUS,
        blank=True,
        default='or',
        help_text='Order Status',
    )

    def is_shipped(self):
        if self.status == 'sh':
            return True
        return False

    def is_canceled(self):
        if self.status == 'cl':
            return True
        return False

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.unit_price = self.product.price
        self.vendor = self.product.vendor
        super(InvoiceProduct, self).save(*args, **kwargs)
        self.invoice.save()

    def delete(self, *args, **kwargs):
        parentInvoice = self.invoice
        super(InvoiceProduct, self).delete(*args, **kwargs)
        parentInvoice.save()
    

    # @property
    # def get_payment_amount(self):
    #     return self.unit_price


class InvoiceService(models.Model):
    """Model representing a service in an order."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular service", editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceListing, on_delete=models.RESTRICT)
    price_paid = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT, blank=True)
    ORDER_STATUS = (
        ('sc', 'Scheduled'),
        ('cl', 'Canceled'),
        ('cm', 'Completed'),
    )
    status = models.CharField(
        max_length=2,
        choices=ORDER_STATUS,
        blank=True,
        default='sc',
        help_text='Order Status',
    )

    def is_completed(self):
        if self.status == 'cm':
            return True
        return False

    def is_canceled(self):
        if self.status == 'cl':
            return True
        return False

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.price_paid = self.service.price
        self.vendor = self.service.vendor
        super(InvoiceService, self).save(*args, **kwargs)
        self.invoice.save()

    def delete(self, *args, **kwargs):
        parentInvoice = self.invoice
        super(InvoiceService, self).delete(*args, **kwargs)
        parentInvoice.save()

    