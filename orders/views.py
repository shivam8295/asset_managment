from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib import messages
from .serializers import OrderDetailSerializer, CustomerDetailSerializer
from asset_master.serializers import *
from .models import *
from .pagination import OrderDetailPagination
from asset_master.pagination import AssetMasterPagination
from django.db.models import Q
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import filters
import csv
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
from django.http import FileResponse, QueryDict
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.tables import Table, TableStyle, colors
from django.forms.models import model_to_dict
import random
from asset_master.models import *






# Create your views here.
def orders_list (request):
    ctx = {}
    if request.user.is_authenticated:
        ctx['user_email']=request.user.email
    return render(request,'orders_list.html', ctx)
        



# class OrderDetailListView(ListAPIView, LoginRequiredMixin):
#     queryset = AssetMaster.objects.all()
#     pagination_class = OrderDetailPagination
#     template_name = 'all_orders_list.html'
#     serializer_class = AssetMasterSerializer
#     filter_backends = [filters.OrderingFilter]
#     authentication_classes = [BasicAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#     ordering = ["-id"]
#     def get_queryset(self, request):
#         query = None
#         filter_type = None
#         if self.request.GET.get('q') is not None:
#             query = self.request.GET.get('q').strip()
#         if self.request.GET.get('filter_type') is not None:
#             filter_type = self.request.GET.get('filter_type').strip()
#         request.session['filter_type'] = filter_type
#         request.session['query'] = query
#         if query and not filter_type:
#             return AssetMaster.objects.filter(
#                 Q(area__icontains=query) |
#                 Q(asset_tag__icontains=query) |
#                 Q(brand__icontains=query) |
#                 Q(category__icontains=query) |
#                 Q(model_no__icontains=query) |
#                 Q(serial_no__icontains=query) |
#                 Q(sku__icontains=query) |
#                 Q(asset_tag__icontains=query) |
#                 Q(status__icontains=query), 
#                 sold_asset=False,
#                 add_to_order=True,
#                 confirm_order=False
#             )
#         elif query and filter_type=='serial_no':
#             return AssetMaster.objects.filter(
#                                             serial_no__iexact=query,
#                                             confirm_order=False,
#                                             add_to_order=True,
#                                             sold_asset=False)
#         elif query and filter_type=='model_no':
#             return AssetMaster.objects.filter(
#                                             model_no__iexact=query,
#                                             confirm_order=False,
#                                             add_to_order=True,
#                                             sold_asset=False)
#         elif query and filter_type=='brand':
#             return AssetMaster.objects.filter(
#                                             brand__iexact=query,
#                                             confirm_order=False,
#                                             add_to_order=True,
#                                             sold_asset=False
#                                             )
        
#         elif query and filter_type=='category':
#             return AssetMaster.objects.filter(
#                                             category__iexact=query,
#                                             confirm_order=False,
#                                             add_to_order=True,
#                                             sold_asset=False
#                                             )
        
#         else:
            
#             asset_obj = list(AssetMaster.objects.filter(
#             sold_asset=False,
#             confirm_order=False,
#             add_to_order=True, 
#             relation=101
#             ).values('id','category','description','serial_no',
#                                         'model_no', 'brand'))
            
#             asset_acc_obj =list( AssetMaster.objects.filter(
#             sold_asset=False,
#             confirm_order=False,
#             add_to_order=True, 
#             relation=102
#             ).values('id','category','description',
#                         'serial_no', 'model_no', 'brand', 'mapping'))

#             for asset in asset_obj:
#                 if 'asset_accessories' not in asset:
#                     asset['asset_accessories'] = []
#                     asset['asset_accessories_description'] = []
                
#                 for asset_acc in asset_acc_obj:
#                     if asset_acc['mapping'] == asset['description']:
#                         if (asset_acc['description']) not in asset['asset_accessories_description']: 
#                             asset['asset_accessories_description'].append(asset_acc['description'])
#                             asset['asset_accessories'].append({
#                                 'description': asset_acc['description'],
#                                 'id':asset_acc['id'],
#                                 'serial_no':asset_acc['serial_no'],
#                                 'model_no':asset_acc['model_no'],
#                                 'brand':asset_acc['brand']
#                             })
#                             asset_acc_obj.remove(asset_acc)
#             # paginator = Paginator(asset_obj, 10) 
#             return asset_obj


            
#     def get(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset(request))
#         queryset_length = len(queryset)
#         query_params_q = None
#         query_params_filter_value = None
#         if request.query_params.get('q') is not None:
#             query_params_q = request.query_params.get('q').strip()
#         if self.request.GET.get('filter_type') is not None:
#             query_params_filter_value = self.request.GET.get('filter_type').strip()
#         page = self.paginate_queryset(queryset)
#         serializer = self.get_serializer(page, many=True)
#         return self.get_paginated_response(serializer.data,
#                     queryset_length, query_params_q, query_params_filter_value, request)

#     def get_paginated_response(self, data, queryset_length, query_params_q, query_params_filter_value, request):
#         ctx = {}
#         ctx = { "query_params_q": query_params_q, "query_params_filter_value": query_params_filter_value} 
#         paginated_assets = self.paginator.page if hasattr(self, 'paginator') else None
#         return render(
#             self.request,
#             self.template_name,
#             {'orders': paginated_assets, 'queryset_length': queryset_length, **ctx}  # Merge assets and context data
#         )




def cart_list_view(request):
    ctx = {}
    asset_obj = list(AssetMaster.objects.filter(
            sold_asset=False,
            confirm_order=False,
            add_to_order=True, 
            relation=101
            ).values('id','category','description','serial_no',
                                'model_no', 'brand', 'add_to_order'))
            
    asset_acc_obj = list(AssetMaster.objects.filter(
            sold_asset=False,
            confirm_order=False,
            add_to_order=True, 
            relation=102
            ).values('id','category','description',
                        'serial_no', 'model_no', 'brand', 'mapping', 'add_to_order'))
    

    asset_obj_ids = [item['id'] for item in asset_obj]
    asset_acc_obj_ids = [item['id'] for item in asset_acc_obj]
    merged_ids = asset_obj_ids + asset_acc_obj_ids


    for asset in asset_obj:
        if 'asset_accessories' not in asset:
            asset['asset_accessories'] = []
            asset['asset_accessories_description'] = []
        
        # Start the index from 0
        index = 0
        while index < len(asset_acc_obj):
            asset_acc = asset_acc_obj[index]
            if asset_acc['mapping'] == asset['description']:
                if asset_acc['description'] not in asset['asset_accessories_description']: 
                    asset['asset_accessories_description'].append(asset_acc['description'])
                    asset['asset_accessories'].append({
                        'description': asset_acc['description'],
                        'id': asset_acc['id'],
                        'serial_no': asset_acc['serial_no'],
                        'model_no': asset_acc['model_no'],
                        'brand': asset_acc['brand'],
                        'category': asset_acc['category']
                    })
                    
                    del asset_acc_obj[index]
                    
                    index = 0
                else:
                    
                    index += 1
            else:
                
                index += 1
    
    asset_accessories_list = []
    for m in asset_obj:
        asset_accessories_list.append(m['asset_accessories'])

    parent_asset_id = []
    for m in asset_obj:
        parent_asset_id.append(m['id'])

    asset_accessories_list_ids = []
    for m in asset_accessories_list:
        for n in m:
            asset_accessories_list_ids.append(n['id'])

    all_category_and_accessory_id = parent_asset_id + asset_accessories_list_ids

    excluded_ids = []
    for m in merged_ids:
        if m not in all_category_and_accessory_id:
            excluded_ids.append(m)


    excluded_obj = []
    for m in asset_acc_obj:
        if m['id'] in excluded_ids:
            excluded_obj.append(m)
        

    ctx["asset_obj"] = asset_obj
    ctx["excluded_obj"] = excluded_obj

    
    return render(request, 'all_orders_list.html', ctx)





@login_required
def export_to_csv_order(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    queryset = OrderDetail.objects.all()
    writer = csv.writer(response)
    writer.writerow(["Order Status", "Organization"])
    for obj in queryset:
        writer.writerow([obj.order_status, obj.organization])  
    return response



#Order detail view...
def orders_info_view(request, id):
    ctx={}
    order_obj=OrderDetail.objects.filter(id=id)
    all_asset_of_an_order = OrderDetail.objects.filter(id=id).values('assets__id','assets__box_number',
    'assets__category', 'assets__description', 'assets__brand', 'assets__serial_no', 'assets__model_no', 
    'assets__owner', 'assets__sub_category', 'order_dispatch', 'approve_order'
    )
    queryset_length = len(all_asset_of_an_order)


    ctx['orders_info'] = order_obj
    ctx['all_asset_of_an_order'] = all_asset_of_an_order
    ctx['queryset_length'] = queryset_length
    return render(request,'orders_info.html',ctx)
  



# class LeftOutAccessoryList(APIView):
#     def get(self, request):
#         order_id = request.query_params.get('id')
#         all_asset_of_an_order = list(OrderDetail.objects.filter(id=order_id)
#                                         .values(
#                                                 'assets__id',
#                                                 'assets__description',
#                                                 'assets__status',
#                                                 "assets__category",
#                                                 'assets__description',
#                                                 'assets__brand',
#                                                 'assets__model_no',
#                                                 'assets__serial_no',
#                                                 'assets__owner',
#                                                 'assets__relation',
#                                                 'assets__mapping',
#                                                 ))
#         description_list = []
#         for asset in all_asset_of_an_order:
#             if asset['assets__description'] not in description_list:
#                 description_list.append(asset['assets__description'])

        
#         all_child_assets = list(AssetMaster.objects.filter(relation=102, mapping__in=description_list))
#         parent_assets = []
#         child_assets = []
#         for asset in all_asset_of_an_order :
#             if asset['assets__relation'] == 101:
#                 parent_assets.append(asset)
#             else:
#                 child_assets.append(asset)
                
#         for asset in parent_assets:
#             if 'asset_accessories' not in asset:
#                 asset['asset_accessories'] = []
#                 asset['asset_accessories_description'] = []
        
#         # Start the index from 0
#             index = 0
#             while index < len(child_assets):
#                 asset_acc = child_assets[index]
#                 if asset_acc['assets__mapping'] == asset['assets__description']:
#                     if asset_acc['assets__description'] not in asset['asset_accessories_description']: 
#                         asset['asset_accessories_description'].append(asset_acc['assets__description'])
#                         asset['asset_accessories'].append({
#                             'description': asset_acc['assets__description'],
#                             'id': asset_acc['assets__id'],
#                             'serial_no': asset_acc['assets__serial_no'],
#                             'model_no': asset_acc['assets__model_no'],
#                             'brand': asset_acc['assets__brand'],
#                             'category': asset_acc['assets__category']
#                         })
                        
#                         del child_assets[index]
                        
#                         index = 0
#                     else:
                        
#                         index += 1
#                 else:
                    
#                     index += 1

        
        
        

        
        
        

#         # items = AssetMaster.objects.all() 
#         # serializer = AssetMasterSerializer(left_out_acc_obj, many=True)
#         return Response("data")




class LeftOutAccessoryList(APIView):
    def get(self, request):
        order_id = request.query_params.get('id')
        all_asset_of_an_order = list(OrderDetail.objects.filter(id=order_id).values_list('assets__id', 'assets__description'))
        asset_ids = [m[0] for m in all_asset_of_an_order]

        order_asset_description = list(([m[1] for m in all_asset_of_an_order]))

        parent_asset = list(AssetMaster.objects.filter(id__in=asset_ids, relation=101).values("id",
                                                                                        "description"))
        
        parent_description_list = list(([m['description'] for m in parent_asset]))
        
        asset_acc_obj = list(AssetMaster.objects.filter(mapping__in=parent_description_list,
                                                        relation=102, add_to_order=False,
                                                        confirm_order=False))
          
        accessories_list = []
        accessories_obj = []
        all_acc = []
        for parent_desc in parent_description_list:
            for asset_acc in asset_acc_obj:
                if asset_acc.description not in accessories_list:
                    accessories_list.append(asset_acc.description)
                    accessories_obj.append(asset_acc)

                
        left_out_acc_list = []
        for m in accessories_list:
            if m not in order_asset_description:
                left_out_acc_list.append(m)


        left_out_acc_obj = []
        for m in accessories_obj:
            if m.description in left_out_acc_list:
                left_out_acc_obj.append(m)        


        # items = AssetMaster.objects.all() 
        serializer = AssetMasterSerializer(left_out_acc_obj, many=True)
        return Response(serializer.data)





class get_data(ListAPIView):
    pagination_class = AssetMasterPagination
    serializer_class = AssetMasterSerializer
    filter_backends = [filters.OrderingFilter]

    def list(self, request, *args, **kwargs):
        if request._request.GET.get('filter_value') and request._request.GET.get('filter_type'):
            filter_value = request._request.GET.get('filter_value')
            filter_type = request._request.GET.get('filter_type')
            if filter_type == 'model_no':
                queryset = AssetMaster.objects.filter(model_no=filter_value)
            if filter_type == 'category':
                queryset = AssetMaster.objects.filter(category=filter_value)
            if filter_type == 'brand':
                queryset = AssetMaster.objects.filter(brand=filter_value)

        elif request._request.GET.get('filter_type') is None and request._request.GET.get('search_field'):
            filter_value = request._request.GET.get('search_field')
            queryset = list(AssetMaster.objects.filter(
            Q(brand__icontains=filter_value) |
            Q(category__icontains=filter_value) |
            Q(model_no__icontains=filter_value) |
            Q(serial_no__icontains=filter_value) |
            Q(description__icontains=filter_value),
            sold_asset=False
        ))
        else:
            queryset = AssetMaster.objects.filter(sold_asset=False)
            
        
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    




#Add asset to order
def add_asset_to_order(request):
    if request.method =='POST':
        asset_id = request.POST.get('asset_id')
        order_id = request.POST.get('order_id')
        order_obj = OrderDetail.objects.filter(id=order_id).first()
        order_attributes = model_to_dict(order_obj) # These three
        order_attributes_with_assets = order_attributes.copy() #Lines are for 
        order_attributes_with_assets_list=order_attributes_with_assets.get('assets') #only observation purpose
        asset_obj = AssetMaster.objects.filter(id=asset_id)
        asset_obj.update(add_to_order=True, confirm_order=True, asset_status="rented_out")
        order_obj.assets.add(AssetMaster.objects.get(id=asset_id))
        order_obj.save()
    return HttpResponse("Success")





#Remove order assets
def remove_asset_from_order(request):
    order_id = request.GET.get('order_id')
    asset_id = request.GET.get('asset_id')
    order_obj=OrderDetail.objects.filter(id=order_id).first()
    order_attributes = model_to_dict(order_obj) # These three
    order_attributes_with_assets = order_attributes.copy() #Lines are for 
    order_attributes_with_assets_list=order_attributes_with_assets.get('assets') #only observation purpose
    asset_id_to_remove = asset_id
    asset_to_remove = AssetMaster.objects.filter(id=asset_id_to_remove)
    asset_to_remove.update(confirm_order=False, asset_status="rented_out")
    order_obj.assets.remove(AssetMaster.objects.get(id=asset_id_to_remove))
    return render(request,'orders_info.html')



#Ready to dispatch
def order_dispatch(request):
    order_id = request.POST.get('order_id')
    five_digit_random_number = str(random.randint(10000, 99999))
    challan_number = 'ZC/'+five_digit_random_number
    order_obj = OrderDetail.objects.filter(id=order_id)
    order_obj.update(order_dispatch=True, challan_number=challan_number, order_status=4)
    response_data = {'success': True, 'message': 'Order dispatch status updated successfully.'}

    customer_details = OrderDetail.objects.filter(id=order_id).values("customer_id__customer",
                                                  "customer_id__deployed_order", "customer_id__taxed",
                                                  "customer_id__email_address", "customer_id__department",
                                                  "customer_id__phone_number", "customer_id__customer_revenue",
                                                  "customer_id__commercial_address", "customer_id__category",
                                                  "customer_id__created_at", "customer_id__secondary_email", 
                                                  "customer_id__description","customer_id__id"
                                                  ).first()  
    
    all_asset_id_list = []
    this_order_asset = OrderDetail.objects.filter(id=order_id).first()
    order_assets = model_to_dict(this_order_asset)
    all_asset_of_order = order_assets.get('assets')
    for asset in all_asset_of_order:
        all_asset_id_list.append(asset.id)

    customer_id = int(customer_details.get('customer_id__id'))
    customer = customer_details.get('customer_id__customer')
    completed_orders = customer_details.get('customer_id__completed_orders')
    deployed_order = customer_details.get('customer_id__deployed_order')
    taxed = customer_details.get('customer_id__taxed')
    email_address = customer_details.get('customer_id__email_address')
    department = customer_details.get('customer_id__department')
    phone_number = customer_details.get('customer_id__phone_number')
    customer_revenue = customer_details.get('customer_id__customer_revenue')
    commercial_address = customer_details.get('customer_id__commercial_address')
    category = customer_details.get('customer_id__category')
    created_at = customer_details.get('customer_id__created_at')
    secondary_email = customer_details.get('customer_id__secondary_email')
    description = customer_details.get('customer_id__description')


    order_history = OrderHistory.objects.create(
        order_id=OrderDetail.objects.get(id=order_id),
        customer_id=customer_id,
        customer=customer,
        completed_orders=completed_orders,
        deployed_order=deployed_order,
        taxed=taxed,
        email_address=email_address,
        department=department,
        phone_number=phone_number,
        customer_revenue=customer_revenue,
        commercial_address=commercial_address,
        category=category,
        created_at=created_at,
        secondary_email=secondary_email,
        description=description
    )
        
    # asset_obj = AssetMaster.objects.filter(id__in=all_asset_id_list)
    # order_history.assets.set(asset_obj)
    # order_history.save()


    #Move to inventory...
    asset_objs = AssetMaster.objects.filter(id__in=all_asset_id_list)
    for asset_obj in asset_objs:
        AssetMasterInventory.objects.create(
            asset_id=asset_obj,
            move_to_inventory=False,
            order_id = order_id
        )

    return JsonResponse(response_data)







#Add Order Post view(Post)
class AssetMasterCustomerPostView(APIView):
    def get(self,request):
        ctx = {}
        return render(request,'add_new_customer.html', ctx)


    def post(self, request):
        ctx = {}
        serializer = CustomerDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "New Customer added.")
            return redirect('/asset_management/all-orders-list/')
        else:
            return render(request, 'order_form.html', ctx)




#Order Post view...
def AssetMasterOrderPostView(request):
    selectedOrderIdsList = []
    if request.method == 'GET':
        ctx = {}
        selectedOrderIds = request.GET.get('selectedOrderIds')
        selectedOrderIdsList = selectedOrderIds.split(",")
        request.session['selectedOrderIdsList'] = selectedOrderIdsList
        customer = CustomerDetail.objects.all()
        ctx['customer'] = customer
        return render(request,'order_form.html', ctx)

    else:
        if request.method == 'POST':
            selectedOrderIdsList = request.session['selectedOrderIdsList']
            customer_id = int(request.POST.get('customer_id'))
            customer_object = CustomerDetail.objects.filter(id=customer_id).first()

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
            approver_email = request.POST.get('approver_email') or None
            checker_email = request.POST.get('checker_email') or None
            maker_email = request.POST.get('maker_email') or None
            truck_details = request.POST.get('truck_details') or None
            driver_details = request.POST.get('driver_details') or None
            customer_name = request.POST.get('customer') or None
            contact_details = request.POST.get('contact_details') or None
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
                checker_email= checker_email,
                maker_email= maker_email,
                truck_details=truck_details,
                driver_details=driver_details,
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
            )
            asset_obj = AssetMaster.objects.filter(id__in=selectedOrderIdsList)
            asset_obj.update(confirm_order=True)
            order_detail.assets.set(asset_obj)
            order_detail.save()

        return redirect('/asset_management/confirmed-orders-list/')




class ConfirmOrderListView(ListAPIView, LoginRequiredMixin):
    pagination_class = OrderDetailPagination
    template_name = 'confirmed_orders_list.html'
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
            return OrderDetail.objects.filter(customer_id__customer__iexact=query)
        # elif query and filter_type=='deployment_date':
        #     return OrderDetail.objects.filter(model_no__iexact=query)
        elif query and filter_type=='order_id':
            return OrderDetail.objects.filter(id=query)
        # elif query and filter_type=='return_date':
        #     return OrderDetail.objects.filter(brand__iexact=query, sold_asset=False, rented_asset=False,
        #         loaned_asset=False, add_to_order=True, confirm_order=False)
        else:
            return OrderDetail.objects.all()
            
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
            {'orders': paginated_assets, 'queryset_length': queryset_length, **ctx}  # Merge assets and context data
        )





def customer_details (request, id):
    ctx={}
    customer_obj = CustomerDetail.objects.filter(id=id)
    customer_obj_files = CustomerAttachFile.objects.filter(customer_id=id)
    customer_obj_comment = CustomerComment.objects.filter(customer_id=id)
    customer_orders = CustomerDetail.objects.filter(id=id).values('orderdetail__id',
    'customer', 'orderdetail__price', 'orderdetail__deployment_date',
    'orderdetail__return_date', 'orderdetail__order_status', 'orderdetail__order_dispatch')
    ctx['attached_files'] = customer_obj_files
    ctx['customer_obj'] = customer_obj
    ctx['customer_orders'] = customer_orders
    ctx['comments'] = customer_obj_comment
    return render(request,'customer_details.html', ctx )




@login_required
def attach_file_to_customer(request):
    fss=FileSystemStorage()        
    file = request.FILES['file']
    id = request.POST['id']
    removed_space_file_name = (file.name).replace(" ", "_")
    files = fss.save(removed_space_file_name, file)
    fileurl = fss.url(files)  
    fileurl=fileurl.lstrip("/")
    fileurl= fileurl.replace("media/","").replace(" ","_")
    customer_obj = CustomerDetail.objects.filter(id=id).first()
    customer_file_obj = CustomerAttachFile.objects.create( 
        customer_id=customer_obj,
        attached_file=fileurl
        )
    return redirect(f'/asset_management/customer-details/{id}/')



@login_required
def attach_file_to_order(request):
    fss=FileSystemStorage()        
    file = request.FILES['file']
    id = request.POST['id']
    removed_space_file_name = (file.name).replace(" ", "_")
    files = fss.save(removed_space_file_name, file)
    fileurl = fss.url(files)  
    fileurl=fileurl.lstrip("/")
    fileurl= fileurl.replace("media/","").replace(" ","_")
    order_obj = OrderDetail.objects.filter(id=id).first()
    order_file_obj = OrderAttachFile.objects.create( 
        order_id=order_obj,
        attached_file=fileurl
        )
    return redirect(f'/asset_management/orderdispatch-details/{id}/')




def update_comment_again_customer(request):
    id = request.POST.get('id')
    customer_obj = CustomerDetail.objects.filter(id=id).first()
    customer_comment_obj = CustomerComment.objects.create(
        date_time = datetime.datetime.now(),
        customer_id = customer_obj,
        comment = request.POST.get('comment')
        )
    
    return redirect(f'/asset_management/customer-details/{id}/')



#Order comment
def update_comment_again_order(request):
    id = request.POST.get('id')
    order_obj = OrderDetail.objects.filter(id=id).first()
    customer_comment_obj = OrderComment.objects.create(
        date_time = datetime.datetime.now(),
        order_id = order_obj,
        comment = request.POST.get('comment')
        )
    
    return redirect(f'/asset_management/orderdispatch-details/{id}/')




# Delete attached file...
def delete_attached_file_order_dispatch(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        OrderAttachFile.objects.get(pk=id).delete()
        messages.success(request, "File deleted")
    return HttpResponse("failed")




def customer_form_edit(request, id):
    ctx={}
    customer_obj = CustomerDetail.objects.filter(id=id)
    ctx['customer_obj'] = customer_obj
    if request.method == 'POST':
        customer=request.POST.get('customer') or None
        completed_orders=request.POST.get('completed_orders') or None
        deployed_order=request.POST.get('deployed_order') or None
        taxed=request.POST.get('taxed') or None
        email_address=request.POST.get('email_address') or None
        department=request.POST.get('department') or None
        phone_number=request.POST.get('phone_number') or None
        customer_revenue=request.POST.get('customer_revenue') or None
        commercial_address=request.POST.get('commercial_address') or None
        category=request.POST.get('category') or None
        created_at=request.POST.get('created_at') or None
        secondary_email=request.POST.get('secondary_email') or None
        description=request.POST.get('description') or None
        customer_obj.update(
            customer=customer,
            completed_orders=completed_orders,
            deployed_order=deployed_order,
            taxed=taxed,
            email_address=email_address,
            department=department,
            phone_number=phone_number,
            customer_revenue=customer_revenue,
            commercial_address=commercial_address,
            created_at=created_at,
            secondary_email=secondary_email,
            category=category,
            description=description,
        )
        customer_obj = CustomerDetail.objects.filter(id=id)
        customer_obj_files = CustomerAttachFile.objects.filter(customer_id=id)
        customer_obj_comment = CustomerComment.objects.filter(customer_id=id)
        customer_orders = CustomerDetail.objects.filter(id=id).values('orderdetail__id',
            'customer', 'orderdetail__price', 'orderdetail__deployment_date',
            'orderdetail__return_date', 'orderdetail__order_status')
        ctx['customer_obj'] = customer_obj
        ctx['comments'] = customer_obj_comment
        ctx['attached_files'] = customer_obj_files
        ctx['customer_orders'] = customer_orders
        return render(request,'customer_details.html', ctx)
    else:
        return render(request,'edit_customer_info.html', ctx)
    


#Edit orders form
def orders_form_edit(request,id):
    ctx = {}
    orders_detail_obj = OrderDetail.objects.filter(id=id)
    if request.method == 'POST':
        name_of_consignee = request.POST.get('name_of_consignee') or None
        invoice_number = request.POST.get('invoice_number') or None
        # quantity = request.POST.get('quantity') or None
        price = request.POST.get('price') or None
        mode_of_dispatch = request.POST.get('mode_of_dispatch') or None
        transportation = request.POST.get('transportation') or None
        order_from = request.POST.get('order_from') or None
        order_to = request.POST.get('order_to') or None
        out_date_and_time = request.POST.get('out_date_and_time') or None
        deployment_date = request.POST.get('deployment_date') or None
        return_date = request.POST.get('return_date') or None
        prepared_by_name = request.POST.get('prepared_by_name') or None
        prepared_by_email = request.POST.get('prepared_by_email') or None
        poc_at_venue_name = request.POST.get('poc_at_venue_name') or None
        approver_email = request.POST.get('approver_email') or None
        checker_email = request.POST.get('checker_email') or None
        maker_email = request.POST.get('maker_email') or None
        truck_details = request.POST.get('truck_details') or None
        contact_details = request.POST.get('contact_details') or None
        driver_details = request.POST.get('driver_details') or None
        organization = request.POST.get('organization') or None
        remarks = request.POST.get('remarks') or None
        purpose = request.POST.get('purpose') or None
        reason = request.POST.get('reason') or None
        office_address = request.POST.get('office_address') or None
        website = request.POST.get('website') or None
        orders_detail_obj.update(
            name_of_consignee=name_of_consignee,
            invoice_number=invoice_number,
            # quantity=quantity,
            price=price,
            mode_of_dispatch=mode_of_dispatch,
            transportation=transportation,
            order_from=order_from,
            order_to=order_to,
            out_date_and_time=out_date_and_time,
            deployment_date=deployment_date,
            return_date=return_date,
            prepared_by_name=prepared_by_name,
            prepared_by_email=prepared_by_email,
            poc_at_venue_name=poc_at_venue_name,
            approver_email=approver_email,
            checker_email=checker_email,
            maker_email=maker_email,
            truck_details=truck_details,
            driver_details=driver_details,
            organization=organization,
            remarks=remarks,
            purpose=purpose,
            reason=reason,
            contact_details=contact_details,
            office_address=office_address,
            website=website,
        )
        return redirect(f"/asset_management/orders-info/{id}/")
    else:
        ctx['orders_detail_obj'] = orders_detail_obj
    return render(request,'orders_formedit.html', ctx)



# Delete attached file...
def customer_attach_file_delete(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        CustomerAttachFile.objects.get(pk=id).delete()
        return HttpResponse("Success")
    else:
        return HttpResponse("Success")


#Order Cart Export to CSV
@login_required
def order_cart_export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    if request.POST.getlist('selected_asset_ids[]') or None:
        selected_ids = request.POST.getlist('selected_asset_ids[]')
        queryset = AssetMaster.objects.filter(id__in=selected_ids)
    else:
        queryset = AssetMaster.objects.filter(add_to_order=True)
    writer = csv.writer(response)
    writer.writerow(["Serial no", "Asset tag", "Brand", "Category", "Area", "Vintage",
                         "Description", "Last service date", "Model no", "Fc no",
                         "Upcoming service date", "In order cart"])
    for obj in queryset:
        writer.writerow([obj.serial_no, obj.asset_tag, obj.brand, obj.category, obj.area, obj.age,
                         obj.description, obj.last_service_date, obj.model_no, obj.fc_no,
                         obj.upcoming_service_date, obj.add_to_order])  
    return response



#Confirmed order Export to CSV
@login_required
def confirmed_order_export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    if request.POST.getlist('selected_asset_ids[]') or None:
        selected_ids = request.POST.getlist('selected_asset_ids[]')
        queryset = OrderDetail.objects.filter(id__in=selected_ids)
    else:
        queryset = OrderDetail.objects.all()
    writer = csv.writer(response)
    writer.writerow(["Order Number", "Customer", "Price", "Deployment Date", "Return Date"])
    for obj in queryset:
        writer.writerow([obj.pk, obj.customer_id.customer, obj.price, obj.deployment_date, obj.return_date])  
    return response




#Auto search for orders cart
def autocomplete_search_orders_cart(request):
    selected_value = request.GET.get('selected_value')
    if selected_value == 'serial_no':
        total_assets = AssetMaster.objects.filter(add_to_order=True, confirm_order=False).values_list('serial_no', flat=True).distinct().order_by('serial_no')
        return JsonResponse(list(total_assets), safe=False)
    
    elif selected_value == 'model_no':
        total_assets = AssetMaster.objects.filter(add_to_order=True, confirm_order=False).values_list('model_no', flat=True).distinct().order_by('model_no')
        return JsonResponse(list(total_assets), safe=False)

    elif selected_value == 'brand':
        total_assets = AssetMaster.objects.filter(add_to_order=True, confirm_order=False).values_list('brand', flat=True).distinct().order_by('brand')
        return JsonResponse(list(total_assets), safe=False)
   
    elif selected_value == 'category':
        total_assets = AssetMaster.objects.filter(add_to_order=True, confirm_order=False).values_list('category', flat=True).distinct().order_by('brand')
        return JsonResponse(list(total_assets), safe=False)
  
    else:
        return JsonResponse([], safe=False)



#Auto search for confirm orders
def autocomplete_search_confirm_orders(request):
    selected_value = request.GET.get('selected_value')
    if selected_value == 'customer_id':
        total_assets = OrderDetail.objects.all().values_list('customer_id__customer', flat=True).distinct().order_by('customer_id__customer')
        return JsonResponse(list(total_assets), safe=False)
    
    elif selected_value == 'deployment_date':
        total_assets = OrderDetail.objects.all().values_list('deployment_date', flat=True).distinct().order_by('deployment_date')
        return JsonResponse(list(total_assets), safe=False)

    elif selected_value == 'order_id':
        total_assets = OrderDetail.objects.all().values_list('id', flat=True).distinct().order_by('id')
        return JsonResponse(list(total_assets), safe=False)
    
    elif selected_value == 'return_date':
        total_assets = OrderDetail.objects.all().values_list('return_date', flat=True).distinct().order_by('return_date')
        return JsonResponse(list(total_assets), safe=False)
  
    else:
        return JsonResponse([], safe=False)
    


@login_required
def generate_order_pdf(request):
    queryset_values = ['orderdetail__id',
    'customer', 'orderdetail__price', 'orderdetail__deployment_date',
    'orderdetail__return_date', 'orderdetail__order_status']
    id = request.GET.get('id')
    buf = io.BytesIO()
    orders_pdf = SimpleDocTemplate(buf, pagesize=letter)
    customer_obj = list(CustomerDetail.objects.filter(id=id).values_list(*queryset_values))
    customer_obj.insert(0, queryset_values)
    t = Table(customer_obj)
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.lightblue)]))
    elemets = []
    elemets.append(t)
    orders_pdf.build(elemets)
    buf.seek(0)
    
    return FileResponse(buf, as_attachment=True, filename='ron.pdf')



#Approve Order
def approve_order(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        order_detail_obj = OrderDetail.objects.filter(id=id).first()
        order_detail_obj.approve_order = True
        order_detail_obj.order_status = 2
        order_detail_obj.save()
    return HttpResponse("Success")



#Approve Order
def cancel_order(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        order_detail_obj = OrderDetail.objects.filter(id=id).first()
        order_assets = model_to_dict(order_detail_obj)
        all_asset_of_order = order_assets.get('assets')
        for m in all_asset_of_order:
            m.confirm_order = False
            m.add_to_order = False
            m.asset_status="available"
            m.save()
        order_detail_obj.approve_order = False
        order_detail_obj.order_status = 3

        order_detail_obj.save()
    return HttpResponse("Success")




#Order history
def order_history_details(request, id):
    ctx={}
    order_history_obj = OrderHistory.objects.filter(id=id).first()
    order_history_obj_ctx = OrderHistory.objects.filter(id=id)
    order_id = order_history_obj.order_id   
    order_assets = model_to_dict(order_id)
    all_asset_of_order = order_assets.get('assets')
    ctx['all_asset_of_order'] = all_asset_of_order
    ctx['order_history_obj_ctx'] = order_history_obj_ctx
    ctx['order_id'] = order_id
    return render(request, 'orders_history.html',ctx)



#Order history
def order_history_list(request):
    ctx={}
    all_dispatched_order = OrderHistory.objects.all()
    queryset_length = len(all_dispatched_order)
    ctx['all_dispatched_order'] = all_dispatched_order
    ctx['queryset_length'] = queryset_length
    return render(request, 'orders_history_list.html',ctx)



