from django.urls import path
from . import views


# ------------
# Public URLs
# ------------
urlpatterns = [
    path('', views.index, name='index'),
    path('vendors/', views.VendorListView.as_view(), name='vendors'),
    path('vendor/<int:pk>', views.VendorDetailView.as_view(), name='vendor-detail'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<uuid:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('service/<uuid:pk>', views.ServiceDetailView.as_view(), name='service-detail'),
]

# ------------
# Vendor URLs
# ------------
urlpatterns += [
    path('manage-products/', views.ManageProductsView.as_view(), name='manage-products'),
    path('manage-services/', views.ManageServicesView.as_view(), name='manage-services'),
]
