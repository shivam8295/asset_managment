from django.urls import path, include
from reports.views import *

urlpatterns = [
    path('assets-reports-list/', asset_reports_table, name='asset_reports_table'),

    #Asset Report main page...
    path('assets-reports-main-page/', asset_report_main_page, name='asset_report_main_page'),

    #Asset report order page...
    path('assets-reports-order-page/', asset_report_order_analysis, name='asset_report_order_analysis'),

    #Ongoing ordes page...
    path('assets-reports-ongoing-orders/', asset_report_ongoing_orders, name='asset_report_ongoing_orders'),
    
    #Completed ordes page...
    path('assets-reports-completed-orders/', asset_report_completed_orders, name='asset_report_completed_orders'),
    
    #Booked ordes page...
    path('assets-reports-booked-orders/', asset_report_booked_orders, name='asset_report_booked_orders'),
    
    #Asset allocated to ordes page...
    path('assets-reports-allocated-to-orders/<int:id>/', asset_allocated_to_orders, name='asset_allocated_to_orders'),

    path('asset-report-of-repair/<str:category>/', asset_report_of_repair, name='asset_report_of_repair'),
    path('category-wise-rented-out-details/<str:category>/', category_wise_rented_out_details, name='category_wise_rented_out_details'),
    path('category-wise-repair-and-maintenace/<str:category>/', category_wise_repair_and_maintenance, name='category_wise_repair_and_maintenance'),
    path('asset-report-out-list/<str:category>/', asset_report_out_list, name='asset_report_out_list'),
    path('asset-category-brand-out-list/<str:category>/', each_category_brand_report, name='each_category_brand_report'),
    path('asset-category-brand-model-out-list/<str:brand>/', each_brand_model_no_report, name='each_brand_model_no_report'),
    
    path('asset-report-out-list-brand-wise/<str:brand>/', asset_report_out_list_brand_wise, name='asset_report_out_list_brand_wise'),
    path('category-brand-wise-rented-out-details/<str:brand>/', category_brand_wise_rented_out_details, name='category_brand_wise_rented_out_details'),
    
    path('asset-report-of-repair-category-brand-wise/<str:brand>/', asset_report_of_repair_category_brand_wise, name='asset_report_of_repair_category_brand_wise'),

    path('asset-report-rented-out-list-model-wise/<str:model_no>/', asset_report_out_list_model_no_wise, name='asset_report_out_list_model_no_wise'),

   path('excess-report-list/', excess_report_list, name='excess_report_list'),
]



