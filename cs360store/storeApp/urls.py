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
# Customer URLs
# ------------
urlpatterns += [
    path('my-orders/', views.MyOrdersListView.as_view(), name='my-orders'),
    path('my-cart/', views.MyCartListView, name='my-cart'),
    path('check-out-cart/', views.CheckOutView, name='check-out'),
    path('my-cart/<uuid:pID>/<int:qty>/add', views.MyCartAddProduct, name='my-cart-add-product'),
    path('my-cart/<uuid:pID>/<int:qty>/remove', views.MyCartRemoveProduct, name='my-cart-remove-product'),
    path('my-cart/<uuid:sID>/add', views.MyCartAddService, name='my-cart-add-service'),
    path('my-cart/<uuid:csID>/remove', views.MyCartRemoveService, name='my-cart-remove-service'),
    path('my-orders/<uuid:pk>', views.MyOrdersDetailView.as_view(), name='my-orders-detail'),
]

# ------------
# Vendor URLs
# ------------
urlpatterns += [
    path('manage-products/', views.ManageProductsView.as_view(), name='manage-products'),
    path('manage-services/', views.ManageServicesView.as_view(), name='manage-services'),
    # path('pending-orders/', views.PendingOrdersView.as_view(), name='pending-orders'),
    # path('fulfilled-orders/', views.FulfilledOrdersView.as_view(), name='fulfilled-orders'),
]

urlpatterns += [
    path('manage-products/create', views.ProductListingCreateView.as_view(), name='create-product'),
    path('manage-services/create', views.ServiceListingCreateView.as_view(), name='create-service'),
    path('manage-products/<uuid:pk>/update', views.ProductListingUpdateView.as_view(), name='update-product'),
    path('manage-services/<uuid:pk>/update', views.ServiceListingUpdateView.as_view(), name='update-service'),
    # path('manage-services/<uuid:pk>/update', views.ServiceListingCreateView.as_view(), name='update-service'),
    # path('manage-products/<uuid:pk>/delete', views.ProductListingDeleteView.as_view(), name='delete-product'),
]