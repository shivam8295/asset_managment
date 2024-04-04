from django.shortcuts import render, redirect
from orders.models import *
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from asset_master.models import * 
from django.db.models import Q
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from orders.serializers import OrderDetailSerializer
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework import filters
from orderdispatch.pagination import OrderDispatchPagination
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4
import io
from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.tables import Table, TableStyle, colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.http import FileResponse
import io
from reportlab.lib.colors import yellow
from reportlab.platypus import KeepInFrame
from reportlab.lib.styles import ParagraphStyle
from django.conf import settings
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus.flowables import KeepTogether
from datetime import datetime
base_url = settings.BASE_URL
from django.db.models import Count


#Order dispatch details
def orderdispatch_details (request, id):
    ctx={}
    order_obj_files = OrderAttachFile.objects.filter(order_id=id)
    order_obj_comment = OrderComment.objects.filter(order_id=id)
    order_obj = OrderDetail.objects.filter(id=id)
    all_asset_of_an_order = OrderDetail.objects.filter(id=id).values('assets__id','assets__box_number',
    'assets__category', 'assets__description', 'assets__brand', 'assets__serial_no', 'assets__model_no', 
    'assets__owner', 'assets__sub_category', 'challan_number','id', 
    'assets__add_to_order', 'return_date'
    )
    asset_obj_inventory_status = AssetMasterInventory.objects.filter(order_id=id).values('move_to_inventory',
                                                'asset_transfer', 'asset_id__id', 'order_id',
                                                'asset_id__description', "asset_id__brand",
                                                'asset_id__model_no', "asset_id__box_number",
                                                "asset_id__category", "asset_id__sub_category",
                                                "asset_id__serial_no")

    duplicate_asset = list(AssetMasterInventory.objects.filter(order_id=1).values("asset_id__id").annotate(duplicate_count=Count('asset_id__id')))
    for i in duplicate_asset:
        if i["duplicate_count"] > 1:
            print(i["asset_id__id"], " : duplicate asset")
    
    customer = CustomerDetail.objects.all()
    ctx['customer'] = customer
    ctx['all_asset_of_an_order'] = all_asset_of_an_order
    ctx['asset_obj_inventory_status'] = asset_obj_inventory_status
    ctx['order_obj'] = order_obj
    ctx['comments'] = order_obj_comment
    ctx['attached_files'] = order_obj_files
    
    return render(request,'orderdispatch_details.html', ctx)




def autocomplete_search_dispatch_orders(request):
    selected_value = request.GET.get('selected_value')
    if selected_value == 'customer_id':
        total_assets = OrderDetail.objects.filter(order_dispatch=True).values_list('customer_id__customer', flat=True).distinct().order_by('customer_id__customer')
        return JsonResponse(list(total_assets), safe=False)
    
    elif selected_value == 'challan_number':
        total_assets = OrderDetail.objects.filter(order_dispatch=True).values_list('challan_number', flat=True).distinct().order_by('challan_number')
        return JsonResponse(list(total_assets), safe=False)

    elif selected_value == 'order_no':
        total_assets = OrderDetail.objects.filter(order_dispatch=True).values_list('id', flat=True).distinct().order_by('id')
        return JsonResponse(list(total_assets), safe=False)
    
    elif selected_value == 'return_date':
        total_assets = OrderDetail.objects.filter(order_dispatch=True).values_list('return_date', flat=True).distinct().order_by('return_date')
        return JsonResponse(list(total_assets), safe=False)
  
    else:
        return JsonResponse([], safe=False)





class DispatchedOrderListView(ListAPIView, LoginRequiredMixin):
    pagination_class = OrderDispatchPagination
    template_name = 'orderdispatch_list.html'
    serializer_class = OrderDetailSerializer
    filter_backends = [filters.OrderingFilter]
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    ordering = ["-id"]
    def get_queryset(self, request):
        query = None
        filter_type = None
        if self.request.GET.get('q') is not None:
            query = self.request.GET.get('q').strip()
        if self.request.GET.get('filter_type') is not None:
            filter_type = self.request.GET.get('filter_type').strip()
        request.session['filter_type'] = filter_type
        request.session['query'] = query
        if query and not filter_type:
            return OrderDetail.objects.filter(
                Q(organization__icontains=query) |
                Q(prepared_by_name__icontains=query),
            )
        elif query and filter_type=='customer_id':
            return OrderDetail.objects.filter(customer_id__customer__iexact=query,
                                               order_dispatch=True)
        
        elif query and filter_type=='challan_number':
            return OrderDetail.objects.filter(challan_number__iexact=query, order_dispatch=True)
        
        elif query and filter_type=='order_no':
            return OrderDetail.objects.filter(id=query, order_dispatch=True)
        
        elif query and filter_type=='return_date':
            return OrderDetail.objects.filter(return_date__iexact=query, order_dispatch=True)
        else:
            return OrderDetail.objects.filter(order_dispatch=True)
            
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(request))
        queryset_length = len(queryset)
        query_params_q = None
        query_params_filter_value = None
        if request.query_params.get('q') is not None:
            query_params_q = request.query_params.get('q').strip()
        if self.request.GET.get('filter_type') is not None:
            query_params_filter_value = self.request.GET.get('filter_type').strip()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data,
                    queryset_length, query_params_q, query_params_filter_value, request)

    def get_paginated_response(self, data, queryset_length, query_params_q, query_params_filter_value, request):
        ctx = {}
        ctx = { "query_params_q": query_params_q, "query_params_filter_value": query_params_filter_value} 
        paginated_assets = self.paginator.page if hasattr(self, 'paginator') else None
        return render(
            self.request,
            self.template_name,
            {'all_dispatched_order': paginated_assets, 'queryset_length': queryset_length, **ctx}  # Merge assets and context data
        )









#Dispatch details
# def orderdispatch_list(request):
#     ctx={}
#     all_dispatched_order = OrderDetail.objects.filter(order_dispatch=True).order_by("-id")
#     ctx['all_dispatched_order'] = all_dispatched_order
#     return render(request,'orderdispatch_list.html', ctx)




#Move back asset to inventory...
def move_asset_to_inventory(request):
    asset_id = request.GET.get('asset_id')
    order_id = request.GET.get('order_id')
    order_obj = OrderDetail.objects.filter(id=order_id).first()
    order_attributes = model_to_dict(order_obj) #These three
    order_attributes_with_assets = order_attributes.copy() #Lines are for
    order_attributes_with_assets_list = order_attributes_with_assets.get('assets') #Only observation purpose
    asset_obj = AssetMaster.objects.filter(id=asset_id)
    move_to_inventory_obj = AssetMasterInventory.objects.filter(asset_id__id=asset_id)
    asset_obj.update(add_to_order=False, confirm_order=False, asset_status="available")
    move_to_inventory_obj.update(move_to_inventory=True)

    # order_obj.assets.remove(AssetMaster.objects.get(id=asset_id))
    # order_obj.save()
    return HttpResponse("Success")




#Order Post view...
def asset_master_transfer_post_view(request):
    selectedAssetsIdsList = []
    if request.method == 'GET':
        ctx = {}
        selectedAssetsIds = request.GET.get('selectedOrderIds')
        order_id = request.GET.get('order_id')
        selectedAssetsIdsList = selectedAssetsIds.split(",")
        request.session['selectedAssetsIdsList'] = selectedAssetsIdsList
        request.session['order_id'] = order_id
        customer = CustomerDetail.objects.all()
        ctx['customer'] = customer
        return render(request,'asset_transfer.html', ctx)

    else:
        if request.method == 'POST':
            selectedAssetsIdsList = request.session['selectedAssetsIdsList']
            order_id = request.session['order_id']
            customer_id = int(request.POST.get('customer_id'))
            customer_object = CustomerDetail.objects.filter(id=customer_id).first()
            # previous_order_obj = OrderDetail.objects.filter(id=order_id).first()
            # for asset_id in selectedAssetsIdsList:
            #     previous_order_obj.assets.remove(AssetMaster.objects.get(id=asset_id))
            asset_inventory_obj = AssetMasterInventory.objects.filter(asset_id__id__in=selectedAssetsIdsList,
                                                                    order_id=order_id)
            for i in asset_inventory_obj:
                if i.asset_transfer == 1 or i.asset_transfer == 2 or i.asset_transfer == 4:
                    return HttpResponse("Please select only approved request...")
                   
            asset_inventory_obj.update(asset_transfer=4)

            price = request.POST.get('price') or None
            deployment_date = request.POST.get('deployment_date') or None
            invoice_number = request.POST.get('invoice_number') or None
            mode_of_dispatch = request.POST.get('mode_of_dispatch') or None
            transportation = request.POST.get('transportation') or None
            order_from = request.POST.get('order_from') or None
            order_to = request.POST.get('order_to') or None
            out_date_and_time = request.POST.get('out_date_and_time') or None
            prepared_by_name = request.POST.get('prepared_by_name') or None
            prepared_by_email = request.POST.get('prepared_by_email') or None
            poc_at_venue_name = request.POST.get('poc_at_venue_name') or None
            maker_email = request.POST.get('maker_email') or None
            checker_email = request.POST.get('checker_email') or None
            approver_email = request.POST.get('approver_email') or None
            truck_details = request.POST.get('truck_details') or None
            customer_name = request.POST.get('customer') or None
            contact_details = request.POST.get('contact_details') or None
            driver_details = request.POST.get('driver_details') or None
            remarks = request.POST.get('remarks') or None
            purpose = request.POST.get('purpose') or None
            reason = request.POST.get('reason') or None
            office_address = request.POST.get('office_address') or None
            website = request.POST.get('website') or None
            return_date = request.POST.get('return_date') or None
            organization = request.POST.get('organization') or None
            # quantity = request.POST.get('quantity') or None
            name_of_consignee = request.POST.get('name_of_consignee') or None
       
            order_detail = OrderDetail.objects.create(
                customer_id=customer_object,
                deployment_date=deployment_date,
                invoice_number=invoice_number,
                mode_of_dispatch=mode_of_dispatch,
                transportation=transportation,
                order_from=order_from,
                price=price,
                order_to=order_to,
                out_date_and_time=out_date_and_time,
                prepared_by_name= prepared_by_name,
                prepared_by_email= prepared_by_email , 
                poc_at_venue_name= poc_at_venue_name,
                approver_email= approver_email,
                maker_email=maker_email,
                checker_email=checker_email,
                truck_details=truck_details,
                customer=customer_name,
                contact_details=contact_details,
                remarks=remarks,
                purpose=purpose,
                reason=reason,
                office_address=office_address,
                website=website,
                return_date=return_date,
                organization=organization,
                # quantity=quantity,
                name_of_consignee=name_of_consignee,
                driver_detailsd=driver_details,
            )
            asset_obj = AssetMaster.objects.filter(id__in=selectedAssetsIdsList)
            order_detail.assets.set(asset_obj)
            order_detail.save()

        return redirect('/asset_management/confirmed-orders-list/')
    

    


def asset_transfer_email(request):
    order_id = request.GET.get('order_id')
    asset_ids = request.GET.get('asset_ids').split(",")
    order_obj = OrderDetail.objects.filter(id=order_id).first() 
    asset_objs = AssetMaster.objects.filter(id__in=asset_ids) 
    user_id = request.user
    move_asset_to_inventory_objs = AssetMasterInventory.objects.filter(asset_id__id__in=asset_ids, order_id=order_id)
    
    for m in move_asset_to_inventory_objs:
        m.asset_transfer = 2
        m.save()
    
    subject = 'Transfer order reminder'
    context = {
        'prepared_by_name': order_obj.prepared_by_name,
        'asset_objs': asset_objs,
        'poc_at_venue_name': order_obj.poc_at_venue_name,
        'user_email_id': user_id,
    }
    html_message = render_to_string('asset_transfer_email.html', context)
    plain_message = strip_tags(html_message)


    
    # Create the email message with both HTML and plain text content
    email = EmailMultiAlternatives(subject, plain_message, 'raunakron00@gmail.com', [order_obj.prepared_by_email, order_obj.approver_email])
    email.attach_alternative(html_message, "text/html")  # Set the HTML content type
    
    # Send the email
    email.send()

    return HttpResponse("Success")





def approve_transfer_request(request):
    try:
        order_id = request.GET.get('order_id')
        poc_at_venue_and_prepared_by_email = OrderDetail.objects.filter(id=order_id).values_list('approver_email', 'prepared_by_email')
        asset_ids = request.GET.get('asset_ids')
        asset_master_inventory_obj = AssetMasterInventory.objects.filter(asset_id__id=asset_ids, order_id=order_id)
        User = CustomUser.objects.filter(Q(email=poc_at_venue_and_prepared_by_email[0][0])
                                        |Q(email=poc_at_venue_and_prepared_by_email[0][1]))

        if request.user in User:
            asset_master_inventory_obj.update(asset_transfer=3)
            messages.success(request, f"The asset is ready to transfer.")
            return HttpResponse('Success')
        else:
            messages.error(request, f"Approver Mail ID {list(poc_at_venue_and_prepared_by_email)}.")
            return HttpResponse('Error')
    except Exception as e:
        messages.error(request, f"Approver Mail ID {list(poc_at_venue_and_prepared_by_email)}.")
        return HttpResponse(f'Error: {str(e)}')


    
from reportlab.lib.pagesizes import landscape

#Print delivery challan...
def print_delivery_challan_pdf(request):
    queryset_values = ["Box No.", "Category", "Description", "Brand", "Model No.", "Serial No", "Remarks"]
    id = request.GET.get('id')
    buf = io.BytesIO()
    custom_page_size = (11*inch, 8*inch)
    # custom_page_size = landscape((9, 6))
    orders_pdf = SimpleDocTemplate(buf, pagesize=custom_page_size, topMargin=0, leftMargin=0, rightMargin=0, bottomMargin=1)
    
    elements = []

    paragraph_text = "Invoice cum packing list"
    paragraph_style = getSampleStyleSheet()['Heading1']
    paragraph_style.alignment = 1
    paragraph_style.backColor = colors.HexColor('#ffc000')
    paragraph = Paragraph(paragraph_text, paragraph_style)
    elements.append(paragraph)
    
    image_path = f"{base_url}/static/images/zoom_logo.png"
    image = Image(image_path, width=inch*2, height=inch*0.7)
    elements.append(image)

    elements.append(Spacer(1, 10))



    paragraph_text = "1A - PLOT No 2022, Old Delhi Gurgaon Road Gurugram - 122001 ( Gurgaon), Haryana, email: info@zoomcom.tv, website : www.zoomcom.tv"
    paragraph_style = ParagraphStyle(name='Normal', fontSize=10, alignment=1)
    
    paragraph = Paragraph(paragraph_text, paragraph_style)

    # Define the width and height of the box
    width = inch * 3
    height = inch * 1  # Adjust height as needed

    boxed_paragraph = KeepInFrame(width, height, [paragraph], hAlign='CENTER')

    # Append the boxed paragraph to the elements list
    elements.append(boxed_paragraph)
    elements.append(Spacer(2, 10))


    additional_details = OrderDetail.objects.filter(id=id).values("transportation",
                                                                  "order_to",
                                                                  "order_from",
                                                                  "deployment_date",
                                                                  "return_date",
                                                                  "truck_details",
                                                                  "driver_details",
                                                                  "contact_details",
                                                                  "invoice_number",
                                                                  "prepared_by_name",
                                                                  "contact_details",
                                                                  "challan_number",
                                                                  "purpose",
                                                                  "id"
                                                                  ).first()


    bold_style = getSampleStyleSheet()['BodyText']
    bold_style.fontName = 'Helvetica-Bold'
    # bold_style.alignment = 1

# Assuming bold_style is defined earlier as mentioned in your code
    if additional_details['deployment_date']:
        deployment_date = datetime.strftime(additional_details['deployment_date'], "%d-%m-%Y")
    else:
        deployment_date = ""

    additional_table_data = [
        (Paragraph(f"<b>Transportation:</b>", bold_style), 
        Paragraph(f"{additional_details['transportation']}"), 
        Paragraph(f"<b>Invoice Number:</b>", bold_style), 
        Paragraph(f"{additional_details['invoice_number']}")),


        (Paragraph(f"<b>Order From:</b>", bold_style), 
        Paragraph(f"{additional_details['order_from']}"),
        Paragraph(f"<b>Order Number:</b>", bold_style), 
        Paragraph(f"{additional_details['id']}")
        ),


        (Paragraph(f"<b>Order To:</b>", bold_style), 
        Paragraph(f"{additional_details['order_to']}"),
        Paragraph(f"<b>Prepared By:</b>", bold_style), 
        Paragraph(f"{additional_details['prepared_by_name']}")
        ),


        (Paragraph(f"<b>Truck Details:</b>", bold_style), 
        Paragraph(f"{additional_details['truck_details']}"),
        Paragraph(f"<b>Challan Number:</b>", bold_style), 
        Paragraph(f"{additional_details['challan_number']}")
        ),


        (Paragraph(f"<b>Driver Details:</b>", bold_style), 
        Paragraph(f"{additional_details['driver_details']}"),
        Paragraph(f"<b>Deployment Date:</b>", bold_style), 
        Paragraph(f"{deployment_date}")
        ),




        (Paragraph(f"<b>Contact Details:</b>", bold_style), 
        Paragraph(f"{additional_details['contact_details']}"),
        Paragraph(f"<b>Return Date:</b>", bold_style), 
        Paragraph(f"{datetime.strftime(additional_details['return_date'], '%d-%m-%Y')}")
        )
    ]

    additional_table = Table(additional_table_data)

    for row_index, row in enumerate(additional_table_data):
        for col_index, cell in enumerate(row):
            additional_table.setStyle(TableStyle([
                ('ALIGN', (col_index, row_index), (col_index, row_index), 'CENTER'),
                ('VALIGN', (col_index, row_index), (col_index, row_index), 'TOP')
            ]))

    additional_table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)]))    

    container_table_data = [
        [additional_table]
    ]

# Now you can use container_table_data as needed in your document

    
    container_table = Table(container_table_data)
    # container_table.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])) 

    width = inch * 7.5
    height = inch * 10  
    boxed_paragraph = KeepInFrame(width, height, [container_table], hAlign='CENTER')   
    elements.append(boxed_paragraph)
        
        
    elements.append(Spacer(1, 10))


    paragraph_text = "Note: Equipment is being sent and to be used for TV broadcast purpose only, Equipment will return to ZOOM COMMUNICATIONS PVT LTD warehouse immediately after completion of event"
    paragraph_style = ParagraphStyle(name='Normal', fontSize=10, alignment=1)
    width = inch * 7
    height = inch * 7

    paragraph = Paragraph(paragraph_text, paragraph_style)
    boxed_paragraph = KeepInFrame(width, height, [paragraph], hAlign='CENTER')
    elements.append(boxed_paragraph)
    elements.append(Spacer(1, 20))
    
    if additional_details['purpose'] is not None:
        paragraph_text = additional_details['purpose']
        paragraph_style = getSampleStyleSheet()['Heading1']
        paragraph_style.alignment = 1
        paragraph_style.backColor = colors.HexColor('#ffc000')
        paragraph = Paragraph(paragraph_text, paragraph_style)
        elements.append(paragraph)
        elements.append(Spacer(1, 20))

    
    if len(request.GET.getlist('assetIds[]')) > 0:
        asset_ids = request.GET.getlist('assetIds[]')
        customer_obj = list(OrderDetail.objects.filter(id=id, assets__id__in=asset_ids).values_list(
                                                                        "assets__box_number",
                                                                        "assets__category",
                                                                        "assets__description",
                                                                        "assets__brand",
                                                                        "assets__model_no", 
                                                                        "assets__serial_no",
                                                                        "remarks"))
    else:
        customer_obj = list(OrderDetail.objects.filter(id=id).values_list(
                                                                        "assets__box_number",
                                                                        "assets__category",
                                                                        "assets__description",
                                                                        "assets__brand",
                                                                        "assets__model_no", 
                                                                        "assets__serial_no",
                                                                        "remarks"))
        
    customer_obj.insert(0, queryset_values)

    table_rows = []
    font_size = 7
    # Iterate through the data and create table rows
    for row in customer_obj:
        table_row = []
        for cell_content in row:
            if cell_content is None or '':
                cell_content = ''
                cell_paragraph = Paragraph(cell_content, ParagraphStyle(name='CellTextStyle',
                                                                        alignment=TA_CENTER,
                                                                        fontSize=font_size))
                table_row.append(cell_paragraph)
            else:
                cell_paragraph = Paragraph(cell_content, ParagraphStyle(name='CellTextStyle',
                                                                        alignment=TA_CENTER,
                                                                        fontSize=font_size))
                table_row.append(cell_paragraph)
        table_rows.append(table_row)
        
    
    table = Table(table_rows, colWidths=[30,80,200,80,150,100, 80])

    # Set table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))



    # width = inch * 8

    # boxed_paragraph = KeepInFrame(width, inch * 100, [table], hAlign='CENTER')
        
    elements.append(table)

    orders_pdf.build(elements)

    buf.seek(0)

    
    return FileResponse(buf, as_attachment=True, filename='delivery_challan.pdf')


