from django.shortcuts import render, redirect
from asset_master.models import *
from repair_maintenance.models import *
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
import csv






def repair_maintenance_list(request):
    ctx = {}
    asset_obj_internal_repair = InternalRepairAndMaintenance.objects.all().order_by("-id")
    asset_obj_external_repair = ExternalRepairAndMaintenance.objects.all().order_by("-id")

    internal_queryset_length = len(asset_obj_internal_repair)
    external_queryset_length = len(asset_obj_external_repair)

    # Number of items per page
    items_per_page = 10

    # Paginate InternalRepairAndMaintenance objects
    paginator_internal = Paginator(asset_obj_internal_repair, items_per_page)
    page_internal = request.GET.get('page_internal')

    try:
        asset_obj_internal_repair = paginator_internal.page(page_internal)
    except PageNotAnInteger:
        asset_obj_internal_repair = paginator_internal.page(1)
    except EmptyPage:
        asset_obj_internal_repair = paginator_internal.page(paginator_internal.num_pages)

    # Paginate ExternalRepairAndMaintenance objects
    paginator_external = Paginator(asset_obj_external_repair, items_per_page)
    page_external = request.GET.get('page_external')

    try:
        asset_obj_external_repair = paginator_external.page(page_external)
    except PageNotAnInteger:
        asset_obj_external_repair = paginator_external.page(1)
    except EmptyPage:
        asset_obj_external_repair = paginator_external.page(paginator_external.num_pages)

    ctx['asset_obj_internal_repair'] = asset_obj_internal_repair
    ctx['asset_obj_external_repair'] = asset_obj_external_repair
    ctx['internal_queryset_length'] = internal_queryset_length
    ctx['external_queryset_length'] = external_queryset_length

    return render(request, 'repair_maintenance_list.html', ctx)






def repair_maintenance_external_details(request, id):
    ctx={}
    repair_obj = ExternalRepairAndMaintenance.objects.filter(id=id)
    external_equipment_details = ExternalEquipmentForwardDetails.objects.filter(external_repair_id=id)
    external_advosory_details = ExternalAdvisoryForEquipmentHandling.objects.filter(external_repair_id=id)
    external_repair_comment = ExternalRepairComment.objects.filter(repair_id=id)
    external_repair_attach_file = ExternalRepairAttachFile.objects.filter(repair_id=id)
    ctx['repair_obj'] = repair_obj
    ctx['external_equipment_details'] = external_equipment_details
    ctx['external_advosory_details'] = external_advosory_details
    ctx['comments'] = external_repair_comment
    ctx['attached_files'] = external_repair_attach_file


    return render(request,'repair_maintenance_external_details.html', ctx)





def repair_maintenance_internal_details (request, id):
    ctx={}
    repair_obj = InternalRepairAndMaintenance.objects.filter(id=id)
    in_details_repair_obj = InDetailsInteranlRepair.objects.filter(internal_repair_id=id)
    spares_repair_obj = SparesInteranlRepair.objects.filter(internal_repair_id=id)
    internal_repair_comment = InternalRepairComment.objects.filter(repair_id=id)
    internal_repair_attach_file = InternalRepairAttachFile.objects.filter(repair_id=id)


    ctx['repair_obj'] = repair_obj
    ctx['in_details_repair_obj'] = in_details_repair_obj
    ctx['spares_repair_obj'] = spares_repair_obj
    ctx['comments'] = internal_repair_comment
    ctx['attached_files'] = internal_repair_attach_file

    # image_obj = model_to_dict(repair_obj.first())
    # if (image_obj.get('signature_of_engineering_head')).url:
    #     image_url = (image_obj.get('signature_of_engineering_head')).url
    #     ctx['image_url'] = image_url


    return render(request,'repair_maintenance_internal_details.html', ctx)





def repair_maintenance_internal_details_edit(request, id):
    if request.method == 'POST':
            internal_repair_obj = InternalRepairAndMaintenance.objects.filter(id=id)
            job_number = request.POST.get('job_number') or None
            price = request.POST.get('price') or None
            organization = request.POST.get('organization') or None
            part_no = request.POST.get('part_no') or None
            quantity = request.POST.get('quantity') or None
            equipment_name = request.POST.get('equipment_name') or None
            equipment_type = request.POST.get('equipment_type') or None
            model_no = request.POST.get('model_no') or None
            serial_no = request.POST.get('serial_no') or None
            accessories = request.POST.get('accessories') or None
            accessories_qty = request.POST.get('accessories_qty') or None
            in_date = request.POST.get('in_date') or None
            in_time = request.POST.get('in_time') or None
            equipment_last_report_date = request.POST.get('equipment_last_report_date') or None
            equipment_last_report_fault = request.POST.get('equipment_last_report_fault') or None
            equipment_received_by = request.POST.get('equipment_received_by') or None
            equipment_received_by_name_section = request.POST.get('equipment_received_by_name_section') or None
            equipment_handed_over_by = request.POST.get('equipment_handed_over_by') or None
            equipment_handed_over_by_name_appt = request.POST.get('equipment_handed_over_by_name_appt') or None
            default_detected = request.POST.get('default_detected') or None
            last_service_date = request.POST.get('last_service_date') or None
            upcoming_service_date = request.POST.get('upcoming_service_date') or None


            equipment_repaired_by = request.POST.get('equipment_repaired_by') or None
            marked_for_oem_date = request.POST.get('marked_for_oem_date') or None
            time_taken_to_repair = request.POST.get('time_taken_to_repair') or None
            equipment_handing_over_date = request.POST.get('equipment_handing_over_date') or None
            equipment_handing_over_signature = request.POST.get('equipment_handing_over_signature') or None
            equipment_received_date = request.POST.get('equipment_received_date') or None
            repair_activity_completion_date = request.POST.get('repair_activity_completion_date') or None
            equipment_receiver_signature = request.POST.get('equipment_receiver_signature') or None


            signature_of_engineering_head = request.FILES.get('signature_of_engineering_head') or None
            signature_of_engineering_inventory_head = request.FILES.get('signature_of_engineering_inventory_head') or None
            
        
       
            _internal_repair_obj = internal_repair_obj.update(
                job_number=job_number,
                price=price,
                organization=organization,
                part_no=part_no,
                quantity=quantity,
                equipment_name=equipment_name,
                equipment_type=equipment_type,
                model_no=model_no,
                serial_no=serial_no,
                accessories=accessories,
                accessories_qty=accessories_qty,
                in_date=in_date,
                in_time=in_time,
                equipment_last_report_date=equipment_last_report_date,
                equipment_last_report_fault=equipment_last_report_fault,
                equipment_received_by=equipment_received_by,
                equipment_received_by_name_section=equipment_received_by_name_section,
                equipment_handed_over_by=equipment_handed_over_by,
                equipment_handed_over_by_name_appt=equipment_handed_over_by_name_appt,
                default_detected=default_detected,
                last_service_date=last_service_date,
                upcoming_service_date=upcoming_service_date,
                

                equipment_repaired_by=equipment_repaired_by,
                repair_activity_completion_date=repair_activity_completion_date,
                marked_for_oem_date=marked_for_oem_date,
                time_taken_to_repair=time_taken_to_repair,
                equipment_handing_over_date=equipment_handing_over_date,
                equipment_handing_over_signature=equipment_handing_over_signature,
                equipment_received_date=equipment_received_date,
                equipment_receiver_signature=equipment_receiver_signature,


                signature_of_engineering_head=signature_of_engineering_head,
                signature_of_engineering_inventory_head=signature_of_engineering_inventory_head,



                
            )
            return redirect(f'/asset_management/repair-maintenance-internal-details/{id}/')
    else:
        ctx={}
        internal_repair_obj = InternalRepairAndMaintenance.objects.filter(id=id)
        ctx['internal_repair_obj'] = internal_repair_obj
        return render(request,'repair_miantenance_internal_edit.html', ctx)



def repair_maintenance_external_details_edit(request, id):
    if request.method == 'POST':
            external_repair_obj = ExternalRepairAndMaintenance.objects.filter(id=id)
            part_no = request.POST.get('part_no') or None
            quantity = request.POST.get('quantity') or None
            equipment_name = request.POST.get('equipment_name') or None
            eqiupment_type = request.POST.get('eqiupment_type') or None
            model_no = request.POST.get('model_no') or None
            serial_no = request.POST.get('serial_no') or None
            accessories = request.POST.get('accessories') or None
            accessories_qty = request.POST.get('accessories_qty') or None
            out_date = request.POST.get('out_date') or None
            out_time = request.POST.get('out_time') or None
            equipment_last_report_date = request.POST.get('equipment_last_report_date') or None
            equipment_last_report_fault = request.POST.get('equipment_last_report_fault') or None
            equipment_received_by = request.POST.get('equipment_received_by') or None
            equipment_handed_over_by = request.POST.get('equipment_handed_over_by') or None
            equipment_handed_over_to = request.POST.get('equipment_handed_over_to') or None
            default_detected = request.POST.get('default_detected') or None
            last_service_date = request.POST.get('last_service_date') or None
            upcoming_service_date = request.POST.get('upcoming_service_date') or None


            #Equipment out details
            repaired = request.POST.get('repaired') or None
            reason = request.POST.get('reason') or None
            specification = request.POST.get('specification') or None
            date_of_intimation = request.POST.get('date_of_intimation') or None
            informed_contact_person = request.POST.get('informed_contact_person') or None
            signature = request.POST.get('signature') or None


            #Equipment received details
            equipment_collected_by = request.POST.get('equipment_collected_by') or None
            quantity_collected = request.POST.get('quantity_collected') or None
            date_of_collection = request.POST.get('date_of_collection') or None
            quantity_received = request.POST.get('quantity_received') or None
            date_of_receipt = request.POST.get('date_of_receipt') or None
            equipment_handed_to_eng_team = request.POST.get('equipment_handed_to_eng_team') or None
            equipment_fitted_in_rack = request.POST.get('equipment_fitted_in_rack') or None


                   
       
            _internal_repair_obj = external_repair_obj.update(
                part_no=part_no,
                quantity=quantity,
                equipment_name=equipment_name,
                eqiupment_type=eqiupment_type,
                model_no=model_no,
                serial_no=serial_no,
                accessories=accessories,
                accessories_qty=accessories_qty,
                out_date=out_date,
                out_time=out_time,
                equipment_last_report_date=equipment_last_report_date,
                equipment_last_report_fault=equipment_last_report_fault,
                equipment_received_by=equipment_received_by,
                equipment_handed_over_by=equipment_handed_over_by,
                equipment_handed_over_to=equipment_handed_over_to,
                default_detected=default_detected,
                last_service_date=last_service_date,
                upcoming_service_date=upcoming_service_date,

                repaired=repaired,
                reason=reason,
                specification=specification,
                date_of_intimation=date_of_intimation,
                informed_contact_person=informed_contact_person,
                signature=signature,

                equipment_collected_by=equipment_collected_by,
                quantity_collected=quantity_collected,
                date_of_collection=date_of_collection,
                quantity_received=quantity_received,
                date_of_receipt=date_of_receipt,
                equipment_handed_to_eng_team=equipment_handed_to_eng_team,
                equipment_fitted_in_rack=equipment_fitted_in_rack


            )
            return redirect(f'/asset_management/repair-maintenance-external-details/{id}/')
    else:
        ctx={}
        external_repair_obj = ExternalRepairAndMaintenance.objects.filter(id=id)
        ctx['external_repair_obj'] = external_repair_obj
        return render(request,'repair_maintenance_external_edit.html', ctx)






#Save InDetails 
def internal_in_details_save(request):
    if request.method == 'POST':
        fault_reported_by_engineer = request.POST.get('fault_reported_by_engineer') or None
        detection_of_fault = request.POST.get('detection_of_fault') or None
        fault_occured = request.POST.get('fault_occured') or None
        type_repairs_carried_out = request.POST.get('type_repairs_carried_out') or None
        internal_repair_id = request.POST.get('repair_id')
        internal_repair_obj = InternalRepairAndMaintenance.objects.filter(id=internal_repair_id).first()


        in_details_interanl_repair_obj = InDetailsInteranlRepair.objects.create(
            internal_repair_id=internal_repair_obj,
            fault_reported_by_engineer=fault_reported_by_engineer,
            detection_of_fault=detection_of_fault,
            fault_occured=fault_occured,
            type_repairs_carried_out=type_repairs_carried_out,
    )

    return HttpResponse("Instance created!")




#Save InDetails 
def internal_repair_spares(request):
    if request.method == 'POST':
        reqmt = request.POST.get('reqmt') or None
        quantity = request.POST.get('quantity') or None
        date_of_demand_requisition = request.POST.get('date_of_demand_requisition') or None
        date_of_receipt = request.POST.get('date_of_receipt') or None
        cost = request.POST.get('cost') or None
        spares_produced_through = request.POST.get('spares_produced_through') or None
        procurement_sanctioned_by = request.POST.get('procurement_sanctioned_by') or None
        signature = request.POST.get('signature') or None
        date_of_fitment = request.POST.get('date_of_fitment') or None
        internal_repair_id = request.POST.get('repair_id') or None
        internal_repair_obj = InternalRepairAndMaintenance.objects.filter(id=internal_repair_id).first()


        in_details_interanl_repair_obj = SparesInteranlRepair.objects.create(
            internal_repair_id=internal_repair_obj,
            reqmt=reqmt,
            quantity=quantity,
            date_of_demand_requisition=date_of_demand_requisition,
            date_of_receipt=date_of_receipt,
            cost=cost,
            date_of_fitment=date_of_fitment,
            spares_produced_through=spares_produced_through,
            procurement_sanctioned_by=procurement_sanctioned_by,
            signature=signature
            
    )

    return HttpResponse("Instance created!")




def external_repair_comment(request):
    id = request.POST.get('id')
    internal_repair_obj = ExternalRepairAndMaintenance.objects.filter(id=id).first()

    repair_obj_comments = ExternalRepairComment.objects.create(
        date_time = datetime.datetime.now(),
        repair_id = internal_repair_obj,
        comment = request.POST.get('comment')
        )
    return HttpResponse("Success")




def internal_repair_comment(request):
    id = request.POST.get('id')
    external_repair_obj = InternalRepairAndMaintenance.objects.filter(id=id).first()

    repair_obj_comments = InternalRepairComment.objects.create(
        date_time = datetime.datetime.now(),
        repair_id = external_repair_obj,
        comment = request.POST.get('comment')
        )
    return HttpResponse("Success")




def attach_file_to_internal_repair(request):
    fss=FileSystemStorage()        
    file = request.FILES['file']
    id = request.POST['id']
    removed_space_file_name = (file.name).replace(" ", "_")
    files = fss.save(removed_space_file_name, file)
    fileurl = fss.url(files)  
    fileurl=fileurl.lstrip("/")
    fileurl= fileurl.replace("media/","").replace(" ","_")
    repair_obj = InternalRepairAndMaintenance.objects.filter(id=id).first()
    repair_file_obj = InternalRepairAttachFile.objects.create( 
        repair_id=repair_obj,
        attached_file=fileurl
        )
    return HttpResponse("Success")




def attach_file_to_external_repair(request):
    fss=FileSystemStorage()        
    file = request.FILES['file']
    id = request.POST['id']
    removed_space_file_name = (file.name).replace(" ", "_")
    files = fss.save(removed_space_file_name, file)
    fileurl = fss.url(files)  
    fileurl=fileurl.lstrip("/")
    fileurl= fileurl.replace("media/","").replace(" ","_")
    repair_obj = ExternalRepairAndMaintenance.objects.filter(id=id).first()
    repair_file_obj = ExternalRepairAttachFile.objects.create( 
        repair_id=repair_obj,
        attached_file=fileurl
        )
    return redirect(f'/asset_management/customer-details/{id}/')





def external_equipment_forward_details_save(request):
    if request.method == 'POST':
        falut_reported = request.POST.get('falut_reported') or None
        falut_detected = request.POST.get('falut_detected') or None
        falut_occured = request.POST.get('falut_occured') or None
        type_of_repair_carried_out = request.POST.get('type_of_repair_carried_out') or None
        external_repair_id = request.POST.get('repair_id')
        external_repair_obj = ExternalRepairAndMaintenance.objects.filter(id=external_repair_id).first()


        in_details_interanl_repair_obj = ExternalEquipmentForwardDetails.objects.create(
            external_repair_id=external_repair_obj,
            falut_reported=falut_reported,
            falut_detected=falut_detected,
            falut_occured=falut_occured,
            type_of_repair_carried_out=type_of_repair_carried_out,
    )

    return HttpResponse("Instance created!")




def external_advisory_details_save(request):
    if request.method == 'POST':
        remarks = request.POST.get('remarks') or None
        external_repair_id = request.POST.get('repair_id')
        external_repair_obj = ExternalRepairAndMaintenance.objects.filter(id=external_repair_id).first()


        in_details_interanl_repair_obj = ExternalAdvisoryForEquipmentHandling.objects.create(
            external_repair_id=external_repair_obj,
            remarks=remarks
    )

    return HttpResponse("Instance created!")





# Delete attached file...
def internal_detail_attach_file_delete(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        InternalRepairAttachFile.objects.get(pk=id).delete()
        return HttpResponse("Success")
    else:
        return HttpResponse("Success")




# Delete attached file...
def external_detail_attach_file_delete(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        ExternalRepairAttachFile.objects.get(pk=id).delete()
        return HttpResponse("Success")
    else:
        return HttpResponse("Success")
    



#Sent for repair...
def send_asset_to_inventory(request):
    if request.method =='POST':
        asset_id = request.POST.get('asset_id')
        asset_obj = AssetMaster.objects.filter(id=asset_id)
        asset_obj.update(asset_status="available", repair_type=10)
    return HttpResponse("Success")





#Internal repair Export to CSV
def internal_repair_export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    if request.POST.getlist('selected_asset_ids[]') or None:
        selected_ids = request.POST.getlist('selected_asset_ids[]')
        queryset = InternalRepairAndMaintenance.objects.all()
    else:
        queryset = InternalRepairAndMaintenance.objects.all()
    writer = csv.writer(response)
    writer.writerow(["Job number", "Price", "organization", "Part no", "Quantity", "Equipment name"
                        ])
    for obj in queryset:
        writer.writerow([obj.job_number, obj.price, obj.organization, obj.part_no, obj.quantity, obj.equipment_name
                        ])  
    return response





#External repair Export to CSV
def external_repair_export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    if request.POST.getlist('selected_asset_ids[]') or None:
        selected_ids = request.POST.getlist('selected_asset_ids[]')
        queryset = ExternalRepairAndMaintenance.objects.all()
    else:
        queryset = ExternalRepairAndMaintenance.objects.all()
    writer = csv.writer(response)
    writer.writerow(["Equipment type", "Equipment Name", "Model No", "Serial No", "Part No"
                    ])
    for obj in queryset:
        writer.writerow([obj.eqiupment_type, obj.equipment_name, obj.model_no, obj.serial_no, obj.part_no
                         ])  
    return response