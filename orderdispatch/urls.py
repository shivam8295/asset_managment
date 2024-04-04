from django.urls import path, include
from orderdispatch.views import *

urlpatterns = [
    # path('orderdispatch-list/', orderdispatch_list, name='orderdispatch_list' ),
    path('orderdispatch-list/', DispatchedOrderListView.as_view(), name='orderdispatch_list' ),
    path('orderdispatch-details/<int:id>/', orderdispatch_details, name='orderdispatch_details'),
    path('move-asset-to-inventory/', move_asset_to_inventory, name='move_asset_to_inventory'),
    path('transfer-form/', asset_master_transfer_post_view, name='asset_master_transfer_post_view'),
    path('send-transfer-email/', asset_transfer_email, name='asset_transfer_email'),
    path('approve-tranfer-request/', approve_transfer_request, name='approve_transfer_request'),
    path('dispatch-order-search/', autocomplete_search_dispatch_orders, name='autocomplete_search_dispatch_orders'),
    path('print-delivery-challan/', print_delivery_challan_pdf, name='print_delivery_challan_pdf'),
]