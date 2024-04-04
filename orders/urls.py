from django.urls import path, include
from orders.views import *

urlpatterns = [

    #Orders 
    path('all-orders-list/', cart_list_view, name='all_orders_list' ),
    # path('all-orders-list/', OrderCartList, name='all_orders_list' ),
    path('orders-form/', AssetMasterOrderPostView, name='orders_form' ),
    path('export-to-csv-order/', export_to_csv_order, name='export_to_csv'), 
    path('orders-info/<int:id>/', orders_info_view, name='orders_info_view'),
    # path('confirmed-order-list/', confirmed_orders_list, name='confirmed_orders_list'),
    path('confirmed-orders-list/', ConfirmOrderListView.as_view(), name='confirmed_order_list'),
    path('orders-form-edit/<int:id>/', orders_form_edit, name='confirmed_orders_list'),

    #Customer
    path('customer-details/<int:id>/', customer_details, name='customer_details'),
    path('add-new-customer/', AssetMasterCustomerPostView.as_view(), name='add_new_customer'),
    path('attach-file-to-customer/', attach_file_to_customer, name='attach_file_to_customer'),
    path('customer-comments/', update_comment_again_customer, name='update_comment_again_customer'),
    path('customer-form-edit/<int:id>/', customer_form_edit, name='orders_formedit' ),
    path('customer-attach-file-delete/', customer_attach_file_delete, name='customer_attach_file_delete'),

    #Export to csv order list
    path('order-cart-export-to-csv/', order_cart_export_to_csv, name='order_cart_export_to_csv'),
    path('confirmed-order-export-to-csv/', confirmed_order_export_to_csv, name='confirmed_order_export_to_csv'),

    #Auto search URL
    path('order-cart-search/', autocomplete_search_orders_cart, name='autocomplete_search_orders_cart'),
    path('confirm-order-search/', autocomplete_search_confirm_orders, name='autocomplete_search_confirm_orders'),
    
    #PDFs
    path('order-detail-pdf/', generate_order_pdf, name='generate_order_pdf'),

    #Approve Order
    path('approve-order/', approve_order, name='approve_order'),

    #Remove asset from order
    path('remove-asset-from-order/', remove_asset_from_order, name='remove_asset_from_order'),

    #Add asset to order
    path('add-asset-to-order/', add_asset_to_order, name='add_asset_to_order'),

    #Cancel Order
    path('cancel-order/', cancel_order, name='cancel_order'),

    #Order dispatch
    path('dispatch-order/', order_dispatch, name='order_dispatch'),


    path('get_data/', get_data.as_view(), name='get_data/'),

    #Alert accessory list
    path('alert-for-accessories/', LeftOutAccessoryList.as_view(), name='left_out_accessory_list'),

    #Attach file to order
    path('attach-file-to-order/', attach_file_to_order, name='attach_file_to_order'),

    #Order comment
    path('add-comment-to-order/', update_comment_again_order, name='update_comment_again_order'),


    #Order attach file delete
    path('order-attach-file-delete/', delete_attached_file_order_dispatch, name='delete_attached_file_order_dispatch'),


    #Orders History
    path('go-to-orders-history/', order_history_list, name='order_history'),
    path('go-to-orders-history-details/<int:id>/', order_history_details, name='order_history_details'),

]

