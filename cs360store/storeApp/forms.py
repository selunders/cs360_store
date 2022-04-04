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

# class BookCreateForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         exclude = ('user',)

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user')
#         super(BookCreateForm, self).__init__(*args, **kwargs)

#     def clean_title(self):
#         title = self.cleaned_data['title']
#         if Book.objects.filter(user=self.user, title=title).exists():
#             raise forms.ValidationError("You have already written a book with same title.")
#         return title


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