from django.contrib import admin
from django.urls import path, include
from asset_master.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Asset Module
    path('asset-form/', AssetMasterPostView.as_view(), name='asset-master'),
    path('asset-list/', AssetListView.as_view(), name='asset_list'),
    path('asset-delete/', AssetMultipleDeleteView.as_view(), name='asset_delete'),
    path('asset-delete/<int:id>/', AssetMultipleDeleteView.as_view(), name='asset_delete_by_id'),
    path('asset-detail/<int:id>/', asset_detail_view, name='asset_detail'),
    path('edit-asset-detail/<int:id>/', update_asset, name='edit_asset_detail'),
    # path('edit-rent-detail/<int:id>/', update_asset, name='edit_rent_detail'),
    path('delete-asset-detail-image/', delete_image, name='delete_asset_detail_image'),
    path('asset-detail-set-availability/', set_availability, name='asset_detail_set_availability'),
    path('asset-detail-set-under-amc/', set_under_amc, name='asset_detail_set_under_amc'),
    path('asset-detail-set-asset-status/', set_asset_status, name='asset_detail_set_asset_status'),
    path('asset-list-search/', autocomplete_search, name='asset_list_search'),

    path('asset-list-search-group-wise/', autocomplete_search_group_wise, name='autocomplete_search_group_wise'),
    
    path('asset-list-acc-search/', autocomplete_acc_search, name='autocomplete_acc_search'),

    path('group-wise-asset-list/', group_wise_asset_list, name='group_wise_asset_list'),
    path('get-group-wise-asset-detail/', GetGroupWiseAssetAccessories.as_view(), name='group_wise_asset_accessories'),

    #Search analytics
    path('asset-list-search-analytics/', autocomplete_search_analytics, name='autocomplete_search_analytics'),
    path('asset-list-search-analytics-brand/', autocomplete_search_analytics_brand, name='autocomplete_search_analytics_brand'),

    path('asset-list-fix-nsn/', fixNSN, name='fix_nsn'),


    #Sold Asset   
    path('sold-list/', SoldAssetListView.as_view(), name='soldasset_list'),
    path('sold-detail/<int:id>/', sold_detail, name='sold_detail'),
    path('edit-sold-detail/', update_sold, name='edit_sold_detail'),
    path('asset-list-sold/', sold_asset, name='edit_sold_detail'),
    path('sold-asset-delete/', SoldAssetMultipleDeleteView.as_view(), name='sold_asset_delete'),


    #Analytics Asset   
    path('analytics-list/', analytics_list, name='analytics_list'),
    path('analytics-category/<str:category>/', analytics_category, name='analytics_category'),
    path('analytics-brand/<str:brand>/', analytics_brand, name='analytics_brand'),


    #Loaned Asset
    path('loan-list/', LoanListView.as_view(), name='loan_list'),
    path('loan-detail/<int:id>/', loan_detail, name='loan_detail'),
    path('edit-loan-detail/<int:id>/', update_loaned_asset, name='edit_loan_detail'),
    path('loan-form/', AssetMasterLoanPostView.as_view(), name='loan_form_post_view'),
    path('loan-asset-delete/', LoanAssetMultipleDeleteView.as_view(), name='loan_asset_delete'),


    #Rent Asset
    path('rent-list/', RentListView.as_view(), name='rent_list'),
    path('rent-detail/<int:id>/', rent_detail, name='rent_detail'),
    path('edit-rent-detail/<int:id>/', update_rented_asset, name='rent_detail'),
    path('rent-form/', AssetMasterRentPostView.as_view(), name='rent_form'),
    path('rent-asset-delete/', RentAssetMultipleDeleteView.as_view(), name='rent_asset_delete'),


    # Upload Excel
    path('upload/', upload_aaset_excel, name='upload_asset_excel'),
    path('upload-sold-asset/', upload_sold_aaset_excel, name='upload_sold_asset_excel'),
    path('upload-loan-asset/', upload_loan_aaset_excel, name='upload_loan_asset_excel'),
    path('upload-rent-asset/', upload_rent_aaset_excel, name='upload_rent_asset_excel'),
    # path('upload-warehouse/', upload_excel_warehouse, name='upload_excel_warehouse'),

    # Dashboard
    path('',home,name='home'),

    # Login & Logout
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    #Frogot password
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'), name='password_reset'),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_success_msg.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),


    # Clone Asset
    path('clone-asset/', clone_asset, name='clone_asset'),

    #Edit comment
    path('edit-asset-detail-comment-again/', update_comment_again, name='edit_asset_detail_comment'),


    #Add to order
    path('add-to-order-asset/', add_to_order, name='add_to_order'),

    #Remove from order
    path('remove-from-order-asset/', remove_from_order, name='remove_from_order'),
    
    
    #Remove from order
    path('send-to-external-repair-asset/', asset_sent_for_external_repair, name='asset_sent_for_external_repair'),

    path('send-to-internal-repair-asset/', asset_sent_for_internal_repair, name='asset_sent_for_internal_repair'),

    # Order Module
    path('asset_management/', include('orders.urls'), name='asset_management_orders'), 

    #Warehouse Module
    # path('asset_management/', include('warehouse.urls'), name='asset_management_warehouse'), 

    #Repair Module
    path('asset_management/', include('repair_maintenance.urls'), name='asset_management_repair_maintenance'), 

    #Order Dispatch Module
    path('asset_management/', include('orderdispatch.urls'), name='asset_management_orderdispatch'), 
    
    
    #Reports
    path('asset_management/', include('reports.urls'), name='asset_management_reports'), 

    #Requiremnts
    path('asset_management/', include('requirements.urls'), name='asset_management_requirements'), 


    # Export to csv file
    path('export-to-csv/', export_to_csv, name='export_to_csv'), 

    # Export to pdf file
    path('export-to-pdf/', generate_asset_pdf, name='export_to_pdf'), 

    # Attach file to asset
    path('attach-file-to-asset/', attach_file_to_asset, name='attach_file_to_asset'), 
    path('asset-management-rented/<int:id>/', rented, name='asset_management_rented'), 
    path('asset-management-outsource/',OutsourceView.as_view(), name='asset_management_outsource'), 

    # Delete Attached file
    path('delete-attached-file/', delete_attached_file, name='delete_attached_file'), 

    # Outsource comment
    path('edit-asset-detail-comment-again-outsource/', update_comment_again_outsource, name='update_comment_again_outsource'), 
    
    path('attach-file-to-outsource/', attach_file_to_asset_outsource, name='attach_file_to_asset_outsource'), 
    
    path('delete-attached-file-outsource/', delete_attached_file_outsource, name='delete_attached_file_outsource'), 

    path('asset-delete-outsource/', AssetMultipleOutsourceDeleteView.as_view(), name='asset_delete_outsource'),




]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


# urlpatterns += staticfiles_urlpatterns()