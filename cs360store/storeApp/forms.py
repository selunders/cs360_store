import datetime

from django import forms
from django.forms import ModelForm
from storeApp.models import ProductListing, ServiceListing

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ProductListingCreateForm(forms.ModelForm):

    class Meta:
        model = ProductListing
        exclude = ('vendor',)

    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop('user').vendor
        super(ProductListingCreateForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        data = self.cleaned_data['name']
        if ProductListing.objects.filter(vendor=self.vendor, name=data).exists():
            raise forms.ValidationError(_("You already have a product with this name."))
        return data
    
    def clean_description(self):
        data = self.cleaned_data['description']
        return data

    def clean_tags(self):
        data = self.cleaned_data['tags']
        return data

class ServiceListingCreateForm(forms.ModelForm):

    class Meta:
        model = ServiceListing
        exclude = ('vendor',)

    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop('user').vendor
        super(ServiceListingCreateForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        data = self.cleaned_data['name']
        if ServiceListing.objects.filter(vendor=self.vendor, name=data).exists():
            raise forms.ValidationError(_("You already have a Service with this name."))
        return data
    
    def clean_description(self):
        data = self.cleaned_data['description']
        return data

    def clean_days_available(self):
        data = self.cleaned_data['days_available']
        return data

    def clean_tags(self):
        data = self.cleaned_data['tags']
        return data