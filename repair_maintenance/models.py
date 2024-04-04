from django.db import models
from asset_master.models import AssetMaster

# Create your models here.

class InternalRepairAndMaintenance(models.Model):
    
    asset_obj = models.ForeignKey(AssetMaster, on_delete=models.CASCADE)
    job_number = models.CharField(null=True, blank=True, max_length=100) 
    price = models.CharField(null=True, blank=True, max_length=100)
    organization = models.CharField(max_length=100, blank=True, null=True)
    part_no = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    equipment_name = models.CharField(null=True, blank=True, max_length=100)
    equipment_type = models.CharField(null=True, blank=True, max_length=100)
    model_no = models.CharField(null=True, blank=True, max_length=100)
    serial_no = models.CharField(null=True, blank=True, max_length=100)
    accessories = models.CharField(null=True, blank=True, max_length=100)
    accessories_qty = models.IntegerField(blank=True, null=True)
    in_date = models.DateField(null=True, blank=True, default=None)
    in_time = models.TimeField(null=True, blank=True, default=None)
    equipment_last_report_date = models.DateField(null=True, blank=True, default=None)
    equipment_last_report_fault = models.CharField(null=True, blank=True, max_length=100)
    equipment_received_by = models.CharField(null=True, blank=True, max_length=100)
    equipment_received_by_name_section = models.CharField(null=True, blank=True, max_length=100)
    equipment_handed_over_by = models.CharField(null=True, blank=True, max_length=100)
    equipment_handed_over_by_name_appt = models.CharField(null=True, blank=True, max_length=100)
    default_detected = models.CharField(null=True, blank=True, max_length=100)
    last_service_date = models.DateField(null=True, blank=True, default=None)
    upcoming_service_date = models.DateField(null=True, blank=True, default=None)


# Out Details
    equipment_repaired_by = models.CharField(null=True, blank=True, max_length=100)
    repair_activity_completion_date = models.DateField(null=True, blank=True, default=None)
    marked_for_oem_date = models.CharField(null=True, blank=True, max_length=100)
    time_taken_to_repair = models.CharField(null=True, blank=True, max_length=100)
    equipment_handing_over_date = models.DateField(null=True, blank=True, default=None)
    equipment_handing_over_signature = models.CharField(null=True, blank=True, max_length=100)
    equipment_received_date = models.DateField(null=True, blank=True, default=None)
    equipment_receiver_signature = models.CharField(null=True, blank=True, max_length=100)


#Signature
    signature_of_engineering_head = models.ImageField(upload_to="media/", default=None, null=True, blank=True)
    signature_of_engineering_inventory_head = models.ImageField(upload_to="media/", default=None, null=True, blank=True)



class InDetailsInteranlRepair(models.Model):
    internal_repair_id = models.ForeignKey(InternalRepairAndMaintenance, on_delete=models.CASCADE)
    fault_reported_by_engineer = models.CharField(null=True, blank=True, max_length=100)
    detection_of_fault = models.CharField(null=True, blank=True, max_length=100)
    fault_occured = models.CharField(null=True, blank=True, max_length=100)
    type_repairs_carried_out = models.CharField(null=True, blank=True, max_length=100)



class SparesInteranlRepair(models.Model):
    internal_repair_id = models.ForeignKey(InternalRepairAndMaintenance, on_delete=models.CASCADE)
    reqmt = models.CharField(null=True, blank=True, max_length=100)
    quantity = models.CharField(null=True, blank=True, max_length=100)
    date_of_demand_requisition = models.CharField(null=True, blank=True, max_length=100)
    date_of_receipt = models.CharField(null=True, blank=True, max_length=100)
    date_of_fitment = models.CharField(null=True, blank=True, max_length=100)
    cost = models.CharField(null=True, blank=True, max_length=100)
    spares_produced_through = models.CharField(null=True, blank=True, max_length=100)
    procurement_sanctioned_by = models.CharField(null=True, blank=True, max_length=100)
    signature = models.CharField(null=True, blank=True, max_length=100)
    



class InternalRepairOutDetails(models.Model):
    internal_repair_id = models.ForeignKey(InternalRepairAndMaintenance, on_delete=models.CASCADE)
    equipment_repaired_by = models.CharField(null=True, blank=True, max_length=100)
    repair_activity_completion_date = models.CharField(null=True, blank=True, max_length=100)
    marked_for_oem_date = models.CharField(null=True, blank=True, max_length=100)
    time_taken_to_repair = models.CharField(null=True, blank=True, max_length=100)
    equipment_handed_over_by = models.CharField(null=True, blank=True, max_length=100)
    equipment_handing_over_date = models.CharField(null=True, blank=True, max_length=100)
    equipment_handing_over_signature = models.CharField(null=True, blank=True, max_length=100)
    equipment_received_by = models.CharField(null=True, blank=True, max_length=100)
    equipment_received_date = models.CharField(null=True, blank=True, max_length=100)
    equipment_receiver_signature = models.CharField(null=True, blank=True, max_length=100)





class InternalRepairAttachFile(models.Model):
    repair_id = models.ForeignKey(InternalRepairAndMaintenance, on_delete= models.CASCADE)
    attached_file = models.FileField(upload_to="media/", default=None, null=True, blank=True)


class InternalRepairComment(models.Model):
    repair_id = models.ForeignKey(InternalRepairAndMaintenance, on_delete= models.CASCADE)
    comment = models.CharField(max_length=100, null=True, blank=True)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)





#----------------------Repair and maintenance external-----------------------#





class ExternalRepairAndMaintenance(models.Model):
    
    asset_obj = models.ForeignKey(AssetMaster, on_delete=models.CASCADE)
    eqiupment_type = models.CharField(null=True, blank=True, max_length=100) 
    equipment_name = models.CharField(null=True, blank=True, max_length=100)
    model_no = models.CharField(null=True, blank=True, max_length=100)
    serial_no = models.CharField(null=True, blank=True, max_length=100)
    part_no = models.CharField(null=True, blank=True, max_length=100)
    quantity = models.CharField(null=True, blank=True, max_length=100)
    accessories = models.CharField(null=True, blank=True, max_length=100)
    accessories_qty = models.CharField(null=True, blank=True, max_length=100)
    out_date = models.DateField(null=True, blank=True, default=None)
    out_time = models.TimeField(null=True, blank=True, default=None)
    equipment_last_report_date = models.DateField(null=True, blank=True, default=None)
    equipment_last_report_fault = models.CharField(null=True, blank=True, max_length=100)
    equipment_received_by = models.CharField(null=True, blank=True, max_length=100)
    equipment_handed_over_by = models.CharField(null=True, blank=True, max_length=100)
    equipment_handed_over_to = models.CharField(null=True, blank=True, max_length=100)
    default_detected = models.CharField(null=True, blank=True, max_length=100)
    last_service_date = models.DateField(null=True, blank=True, default=None)
    upcoming_service_date = models.DateField(null=True, blank=True, default=None)


    #Equipment Out Details
    repaired = models.CharField(null=True, blank=True, max_length=100)
    specification = models.CharField(null=True, blank=True, max_length=100)
    reason = models.CharField(null=True, blank=True, max_length=100)
    date_of_intimation = models.DateField(null=True, blank=True, default=None)
    informed_contact_person = models.CharField(null=True, blank=True, max_length=100)
    signature = models.CharField(null=True, blank=True, max_length=100)
    


    #Equipment received details
    equipment_collected_by = models.CharField(null=True, blank=True, max_length=100)
    quantity_collected = models.CharField(null=True, blank=True, max_length=100)
    date_of_collection = models.DateField(null=True, blank=True, default=None)
    quantity_received = models.CharField(null=True, blank=True, max_length=100)    
    date_of_receipt = models.DateField(null=True, blank=True, default=None)
    equipment_handed_to_eng_team = models.CharField(null=True, blank=True, max_length=100)    
    equipment_fitted_in_rack = models.CharField(null=True, blank=True, max_length=100)






class ExternalEquipmentForwardDetails(models.Model):
    external_repair_id = models.ForeignKey(ExternalRepairAndMaintenance, on_delete=models.CASCADE)
    falut_reported = models.CharField(null=True, blank=True, max_length=100)
    falut_detected = models.CharField(null=True, blank=True, max_length=100)
    falut_occured = models.CharField(null=True, blank=True, max_length=100)
    type_of_repair_carried_out = models.CharField(null=True, blank=True, max_length=100)




class ExternalAdvisoryForEquipmentHandling(models.Model):
    external_repair_id = models.ForeignKey(ExternalRepairAndMaintenance, on_delete=models.CASCADE)
    remarks = models.CharField(null=True, blank=True, max_length=100)
    


class ExternalRepairAttachFile(models.Model):
    repair_id = models.ForeignKey(ExternalRepairAndMaintenance, on_delete= models.CASCADE)
    attached_file = models.FileField(upload_to="media/", default=None, null=True, blank=True)


class ExternalRepairComment(models.Model):
    repair_id = models.ForeignKey(ExternalRepairAndMaintenance, on_delete= models.CASCADE)
    comment = models.CharField(max_length=100, null=True, blank=True)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
