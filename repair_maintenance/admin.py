from django.contrib import admin
from repair_maintenance.models import *

# Register your models here.


@admin.register(InternalRepairAndMaintenance)
class InternalRepairAndMaintenanceAdmin(admin.ModelAdmin):
    list_display = ["id", "equipment_name", "model_no", "serial_no"]



@admin.register(InDetailsInteranlRepair)
class InDetailsInternalRepairAdmin(admin.ModelAdmin):
    list_display = ["id", "internal_repair_id", "fault_reported_by_engineer", "detection_of_fault", "fault_occured", "type_repairs_carried_out"]




@admin.register(SparesInteranlRepair)
class SparesInternalRepairAdmin(admin.ModelAdmin):
    list_display = ["id", "reqmt", "quantity", "date_of_demand_requisition", "date_of_receipt", "date_of_fitment"]




@admin.register(InternalRepairOutDetails)
class InternalRepairOutDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "equipment_repaired_by", "repair_activity_completion_date", "marked_for_oem_date"]




@admin.register(InternalRepairAttachFile)
class InternalRepairAttachFileAdmin(admin.ModelAdmin):
    list_display = ["id", "attached_file"]



@admin.register(InternalRepairComment)
class InternalRepairCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "comment", "date_time"]



#----------------------------External repair and maintenance--------------------------------#
    


@admin.register(ExternalRepairAndMaintenance)
class ExternalRepairAndMaintenanceAdmin(admin.ModelAdmin):
    list_display = ["id", "eqiupment_type", "equipment_name", "model_no", "serial_no", "part_no"]



@admin.register(ExternalEquipmentForwardDetails)
class ExternalEquipmentForwardDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "falut_reported", "falut_detected", "falut_occured", "type_of_repair_carried_out"]



@admin.register(ExternalAdvisoryForEquipmentHandling)
class ExternalAdvisoryForEquipmentHandlingAdmin(admin.ModelAdmin):
    list_display = ["id", "external_repair_id", "remarks"]





@admin.register(ExternalRepairAttachFile)
class ExternalRepairAttachFileAdmin(admin.ModelAdmin):
    list_display = ["id", "attached_file", "repair_id"]




@admin.register(ExternalRepairComment)
class ExternalRepairCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "comment", "date_time"]








