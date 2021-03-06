from django.urls import path, re_path
from . import views


# ------------
# Public URLs
# ------------
urlpatterns = [
    path('', views.index, name='index'),
    path('vendors/', views.VendorListView.as_view(), name='vendors'),
    path('vendor/<int:pk>', views.VendorDetailView.as_view(), name='vendor-detail'),
    path('products/', views.ProductListView.as_view(), name='products'),
    # path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<uuid:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    # re_path(r'products/search/best-match/??(?:&?[^=&]*=[^=&]*)*', views.ProductSearchRankedView, name='product-search-best-match'),
    path('products/search/<str:type>/', views.ProductSearchView, name='product-search'),
    # re_path(r'products/search/closest/??(?:&?[^=&]*=[^=&]*)*', views.ProductSearchClosestRankedView, name='product-search-closest'),
    # re_path(r'products/search/exact-match/??(?:&?[^=&]*=[^=&]*)*', views.ProductSearchRankedExactView, name='product-search-exact'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('service/<uuid:pk>', views.ServiceDetailView.as_view(), name='service-detail'),
    # path('tags/', views.ServiceListView.as_view(), name='tags'),
    # path('products/tag/<str:pk>/', views.ProductTagDetailView, name='product-tag-detail'),
    path('products/tag/<str:pk>/<int:page>', views.ProductTagDetailView, name='product-tag-detail'),
    path('services/tag/<str:pk>/<int:page>', views.ServiceTagDetailView, name='service-tag-detail'),
]

# ------------
# Customer URLs
# ------------
urlpatterns += [
    path('my-orders/', views.MyOrdersListView.as_view(), name='my-orders'),
    path('my-cart/', views.MyCartListView, name='my-cart'),
    path('check-out-cart/', views.CheckOutView, name='check-out'),
    path('my-cart/add/<uuid:pID>', views.MyCartAddProduct, name='my-cart-add-product'),
    path('my-cart/<uuid:pID>/remove', views.MyCartRemoveProduct, name='my-cart-remove-product'),
    path('my-cart/<uuid:csID>/add', views.MyCartAddService, name='my-cart-add-service'),
    path('my-cart/remove/<uuid:csID>', views.MyCartRemoveService, name='my-cart-remove-service'),
    path('my-orders/<uuid:pk>', views.MyOrdersDetailView.as_view(), name='my-orders-detail'),
]

# ------------
# Vendor URLs
# ------------
urlpatterns += [
    path('manage-products/', views.ManageProductsView.as_view(), name='manage-products'),
    path('manage-services/', views.ManageServicesView.as_view(), name='manage-services'),
    path('manage-product-orders/', views.ManageProductOrdersView.as_view(), name='manage-product-orders'),
    path('manage-service-orders/', views.ManageServiceOrdersView.as_view(), name='manage-service-orders'),
    path('manage-product-orders/update/<uuid:ipID>/<str:status>/', views.InvoiceProductStatusUpdate, name='change-product-order-status'),
    path('manage-service-orders/update/<uuid:isID>/<str:status>/', views.InvoiceServiceStatusUpdate, name='change-service-order-status'),
    # path('manage-product-orders/update/<uuid:pk>/<bool:status>/', views.InvoiceProductStatusUpdate, name='change-order-status'),
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