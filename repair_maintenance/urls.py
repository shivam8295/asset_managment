from django.urls import path, include
from repair_maintenance.views import *

urlpatterns = [
    path('repair-maintenance-list/', repair_maintenance_list, name='repair_maintenance_list' ),
    path('repair-maintenance-internal-details/<int:id>/', repair_maintenance_internal_details, name='repair_maintenance_internal_details'),
    path('repair-maintenance-internal-edit/<int:id>/', repair_maintenance_internal_details_edit, name='repair_maintenance_internal_details'),
    path('repair-maintenance-external-details/<int:id>/', repair_maintenance_external_details, name='repair_maintenance_external_details'),
    path('repair-maintenance-external-edit/<int:id>/', repair_maintenance_external_details_edit, name='repair_maintenance_external_details'),
    path('save-in-details-repair/', internal_in_details_save, name='internal_in_details_save'),
    path('save-spare-internal-repair/', internal_repair_spares, name='internal_repair_spares'),


    path('external-equipment-forward-details-save/', external_equipment_forward_details_save, name='external_equipment_forward_details_save'),
    path('external-advisory-details-save/', external_advisory_details_save, name='external_advisory_details_save'),


    path('external-repair-comments/', external_repair_comment, name='external_repair_comment'),
    path('internal-repair-comments/', internal_repair_comment, name='external_repair_comment'),


    path('internal-repair-attach-file/', attach_file_to_internal_repair, name='attach_file_to_internal_repair'),
    path('external-repair-attach-file/', attach_file_to_external_repair, name='attach_file_to_external_repair'),


    path('internal-detail-attach-file-delete/', internal_detail_attach_file_delete, name='internal_detail_attach_file_delete'),
    path('external-detail-attach-file-delete/', external_detail_attach_file_delete, name='external_detail_attach_file_delete'),


    path('send-to-asset-to-inventory/', send_asset_to_inventory, name='send_asset_to_inventory'),


    path('internal-repair-export-to-csv/', internal_repair_export_to_csv, name='internal_repair_export_to_csv'),
    path('external-repair-export-to-csv/', external_repair_export_to_csv, name='external_repair_export_to_csv'),

]