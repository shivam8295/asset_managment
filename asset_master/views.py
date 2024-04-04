from django.shortcuts import render
from .forms import ExcelUploadForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import AssetMasterSerializer
import pandas as pd
from rest_framework.generics import ListAPIView
from .pagination import AssetMasterPagination
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, logout
from rest_framework import filters
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import authentication_classes, permission_classes, api_view
# from warehouse.models import Warehouse
import csv
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
from django.http import FileResponse, QueryDict
import datetime
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from orders.models import *
from repair_maintenance.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse





#Add Asset view(Post)
class AssetMasterPostView(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        ctx = {}
        asset_description = list(AssetMaster.objects.filter(
                relation=101,
                sold_asset=False,
                rented_asset=False,
                loaned_asset=False,).values_list('description').distinct())
        
        asset_description = [item[0] for item in asset_description]        

        ctx['asset_description'] = asset_description
        return render(request,'asset_form.html', ctx)


    def post(self, request):
        ctx = {}
        ctx['user_email']=request.user.email
        form_data = request.data

        if 'relation' not in form_data:
            return HttpResponse("Please provide a value for the 'relation' field")
        elif request.data['relation'] == '102' and request.data['mapping'] == '': 
            return HttpResponse("Please select a mapping field")

        serializer = AssetMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "New Asset added.")
            return redirect('/asset-list/')
        else:
            # messages.add_message(request, f'{serializer.error_messages['required']}')
            ctx['form_data'] = form_data
            return render(request, 'asset_form.html', ctx)


#Update Asset
@login_required
# @api_view(['GET', 'POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def update_asset(request, id):
    ctx={}
    query=""
    asset_obj = AssetMaster.objects.filter(pk=id)
    serial_no = [asset.serial_no for asset in asset_obj]
    if request.user.is_authenticated:
        ctx['user_email']=request.user.email
    ctx['assets'] = asset_obj
    fss=FileSystemStorage()        
    if request.method == 'POST':
        model_no = request.POST.get('model_no')
        if request.FILES.get('image'):
            file = request.FILES.get('image')
            files = fss.save(file.name, file)
            fileurl = fss.url(files)  
            fileurl=fileurl.lstrip("/")
            fileurl= fileurl.replace("media/","")
        serial_no=request.POST.get('serial_no',None)
        category=request.POST.get('category',None)
        sub_category=request.POST.get('sub_category',None)
        asset_tag=request.POST.get('asset_tag',None)
        brand=request.POST.get('brand',None)
        sku=request.POST.get('sku',None)
        fc_no=request.POST.get('fc_no',None)
        description=request.POST.get('description',None)
        status=request.POST.get('status',None)
        age=request.POST.get('age',None) 
        box_number=request.POST.get('box_number',None) 
        last_service_date=request.POST.get('last_service_date') or None
        upcoming_service_date=request.POST.get('upcoming_service_date') or None

        #Unit of measurement
        length=request.POST.get('length',None) 
        breadth=request.POST.get('breadth',None)
        width=request.POST.get('width',None) 
        height=request.POST.get('height',None)

        #Product Engineering Support Info
        warranty_period=request.POST.get('warranty_period',None)
        amc_date=request.POST.get('amc_date') or None

        #Asset In and Out Tracking
        storage_warehouse_number=request.POST.get('storage_warehouse_number',None)
        outward_date=request.POST.get('outward_date') or None
        outward_remarks=request.POST.get('outward_remarks',None)
        inward_date=request.POST.get('inward_date') or None
        inward_remarks=request.POST.get('inward_remarks',None)

        #Purchase
        vendor=request.POST.get('vendor',None)
        purchased_on=request.POST.get('purchased_on') or None
        cost_price=request.POST.get('cost_price',None)
        tax_rate=request.POST.get('tax_rate',None)
        depricated_value=request.POST.get('depricated_value',None)
        created_on=request.POST.get('created_on') or None

        #Pricing
        rental_pricing=request.POST.get('rental_pricing',None)
        rent_collected=request.POST.get('rent_collected',None)
        available_for_sale=request.POST.get('available_for_sale',None)

        #Usage Information
        asset_utilization=request.POST.get('asset_utilization',None)

        #Owner
        owner=request.POST.get('owner',None)


        #Asset status
        # asset_status=request.POST.get('asset_status',None)

        

        if request.FILES.get('image'):
            asset_obj.update( 
            image=fileurl,
            model_no=model_no,
            serial_no=serial_no,
            category = category,
            sub_category=sub_category,
            asset_tag = asset_tag,
            brand = brand,
            sku = sku,
            fc_no = fc_no,
            description = description,
            status = status,
            age = age,
            box_number = box_number,
            last_service_date = last_service_date,
            upcoming_service_date = upcoming_service_date,

            #Unit of measurement
            length=length,
            breadth=breadth,
            width=width,
            height=height,


            warranty_period=warranty_period,
            storage_warehouse_number=storage_warehouse_number,
            outward_date=outward_date,
            outward_remarks=outward_remarks,
            inward_date=inward_date,
            inward_remarks=inward_remarks,
            vendor=vendor,
            purchased_on=purchased_on,
            cost_price=cost_price,
            tax_rate=tax_rate,
            depricated_value=depricated_value,
            created_on=created_on,
            rental_pricing=rental_pricing,
            rent_collected=rent_collected,
            available_for_sale=available_for_sale,
            asset_utilization=asset_utilization,
            owner=owner

            )
        else:
            asset_obj.update(
            model_no=model_no,
            serial_no=serial_no,
            category = category,
            sub_category=sub_category,
            asset_tag = asset_tag,
            brand = brand,
            sku = sku,
            fc_no = fc_no,
            description = description,
            status = status,
            age = age,
            box_number = box_number,
            last_service_date = last_service_date,
            upcoming_service_date = upcoming_service_date,

            #Unit of measurement
            length=length,
            breadth=breadth,
            width=width,
            height=height,

            #Product Engineering Support Info
            warranty_period=warranty_period,
            amc_date=amc_date,

            #Asset In and Out Tracking
            storage_warehouse_number=storage_warehouse_number,
            outward_date=outward_date,
            outward_remarks=outward_remarks,
            inward_date=inward_date,
            inward_remarks=inward_remarks,

            #Purchase
            vendor=vendor,
            purchased_on=purchased_on,
            cost_price=cost_price,
            tax_rate=tax_rate,
            depricated_value=depricated_value,
            created_on=created_on,

            #Pricing
            rental_pricing=rental_pricing,
            rent_collected=rent_collected,
            available_for_sale=available_for_sale,

            #Usage Information
            asset_utilization=asset_utilization,

            owner=owner,
            )    
        if request.session['query'] and not request.session['filter_type']:
            query=request.session['query']   
            messages.success(request, f"Asset details with Serial No.{serial_no} updated.")
            return redirect(f'/asset-list/?q={query}')
        if request.session['query'] and request.session['filter_type']:
            query=request.session['query']
            filter_type=request.session['filter_type']
            messages.success(request, f"Asset details with Serial No.{serial_no} updated.")
            return redirect(f'/asset-list/?q={query}&filter_type={filter_type}')
        messages.success(request, f"Asset details with Serial No.{serial_no} updated.")
        # del request.session['query']
        return redirect(f'/asset-list/')       
    else:
        return render(request, 'edit_asset_detail.html', ctx)


#Autocomplete search
# def autocomplete_search(request):
    # if 'term' in request.GET:
    #     query = request.GET.get('term')
        # total_assets = AssetMaster.objects.values('category').distinct()
        # total_categories = AssetMaster.objects.filter(category__icontains=query).values('category')
        # search = list()
        # for qs in total_assets:
        #     search.append(qs['category'])
        # return JsonResponse(search, safe=False)
    # return render(request, 'asset_list.html')
        # return total_assets


def autocomplete_search(request):
    selected_value = request.GET.get('selected_value')
    if selected_value == 'category':
        total_assets = AssetMaster.objects.values_list('category', flat=True).distinct().order_by('category')
        return JsonResponse(list(total_assets), safe=False)
    
    elif selected_value == 'model_no':
        total_assets = AssetMaster.objects.values_list('model_no', flat=True).distinct().order_by('model_no')
        return JsonResponse(list(total_assets), safe=False)

    elif selected_value == 'brand':
        total_assets = AssetMaster.objects.values_list('brand', flat=True).distinct().order_by('brand')
        return JsonResponse(list(total_assets), safe=False)
  
    else:
        return JsonResponse([], safe=False)


def autocomplete_search_analytics(request):
    selected_value = request.GET.get('selected_value')
    if selected_value == 'category':
        total_assets = AssetMaster.objects.values_list('category', flat=True).distinct().order_by('category')
        return JsonResponse(list(total_assets), safe=False)
    
    elif selected_value == 'model_no':
        total_assets = AssetMaster.objects.values_list('model_no', flat=True).distinct().order_by('model_no')
        return JsonResponse(list(total_assets), safe=False)

    elif selected_value == 'brand':
        total_assets = AssetMaster.objects.values_list('brand', flat=True).distinct().order_by('brand')
        return JsonResponse(list(total_assets), safe=False)
  
    else:
        return JsonResponse([], safe=False)


def autocomplete_search_analytics_brand(request):
    selected_value = request.GET.get('selected_value')
    category=request.session['category']

    if selected_value == 'brand':
        total_assets = AssetMaster.objects.filter(category__iexact=category).values_list('brand', flat=True).distinct().order_by('brand')
        return JsonResponse(list(total_assets), safe=False)
  
    else:
        return JsonResponse([], safe=False)




def autocomplete_acc_search(request):
    selected_value = request.GET.get('selected_value')
    if selected_value == 'category':
        total_assets = AssetMaster.objects.filter(relation=102).values_list('category', flat=True).distinct().order_by('category')
        return JsonResponse(list(total_assets), safe=False)
    
    elif selected_value == 'model_no':
        total_assets = AssetMaster.objects.filter(relation=102).values_list('model_no', flat=True).distinct().order_by('model_no')
        return JsonResponse(list(total_assets), safe=False)

    elif selected_value == 'brand':
        total_assets = AssetMaster.objects.filter(relation=102).values_list('brand', flat=True).distinct().order_by('brand')
        return JsonResponse(list(total_assets), safe=False)
  
    else:
        return JsonResponse([], safe=False)




#Sold Asset
def sold_asset(request):
    id = request.POST.get('id')
    AssetMaster.objects.filter(pk=id).update( 
        sold_asset = True,
        )
    return render(request, 'assest_list.html')


#Add to order
def add_to_order(request):
    asset_id = request.POST.get('asset_id')
    AssetMaster.objects.filter(pk=asset_id).update( 
        add_to_order = True,
        asset_status = "rented_out"
        )
    return render(request, 'assest_list.html')


#Remove from order
def remove_from_order(request):
    asset_id = request.POST.get('asset_id')
    AssetMaster.objects.filter(pk=asset_id).update( 
        add_to_order = False,
        asset_status = "available"
        )
    return redirect('/asset_management/all-orders-list/')



#Sent for repair...
def asset_sent_for_external_repair(request):
    if request.method =='POST':
        asset_id = request.POST.get('asset_id')
        asset_obj = AssetMaster.objects.filter(id=asset_id)
        asset_in_order = None
        asset_in_confirmed_order = None
        for m in asset_obj:
            asset_in_order = m.add_to_order
            asset_in_confirmed_order = m.confirm_order
        if asset_in_order == True or asset_in_confirmed_order == True:
            return HttpResponse("This order is booked")
        asset_obj.update(asset_status="sent_for_repair", repair_type=20)



        asset_get = AssetMaster.objects.get(id=asset_id)
        model_no = asset_get.model_no
        serial_no = asset_get.serial_no
        description = asset_get.description

        
        # Create ExternalRepairAndMaintenance object
        create_repair_obj = ExternalRepairAndMaintenance.objects.create(
            asset_obj=asset_get,
            model_no=model_no,
            serial_no=serial_no,
            equipment_name=description
        )

        
    return HttpResponse("Success")



#Internl repair...
def asset_sent_for_internal_repair(request):
    if request.method =='POST':
        asset_id = request.POST.get('asset_id')
        asset_obj = AssetMaster.objects.filter(id=asset_id)

        asset_in_order = None
        asset_in_confirmed_order = None
        for m in asset_obj:
            asset_in_order = m.add_to_order
            asset_in_confirmed_order = m.confirm_order
        if asset_in_order == True or asset_in_confirmed_order == True:
            return HttpResponse("This order is booked")

        asset_obj.update(asset_status="sent_for_repair", repair_type=30)



        asset_get = AssetMaster.objects.get(id=asset_id)
        model_no = asset_get.model_no
        serial_no = asset_get.serial_no
        description = asset_get.description

        
        # Create InternalRepairAndMaintenance object
        create_repair_obj = InternalRepairAndMaintenance.objects.create(
            asset_obj=asset_get,
            model_no=model_no,
            serial_no=serial_no,
            equipment_name=description
        )



    return HttpResponse("Success")




#Fix NSN
def fixNSN(request):
    all_asset_obj = AssetMaster.objects.filter(Q(serial_no__icontains='NSN'))
    k=1
    for i in all_asset_obj:
        serial_no = i.serial_no + str(k)
        id=i.id
        AssetMaster.objects.filter(pk=id).update( 
        serial_no = serial_no)     
        k=k+1
    return all_asset_obj





@login_required
def update_comment_again(request):
    id = request.POST.get('id')
    ctx={}
    asset_obj = AssetMasterComment.objects.create(
        date_time = datetime.datetime.now(),
        asset_id = id,
        comment = request.POST.get('comment')
        )
    
    ctx['comments'] = asset_obj
    return redirect(f'/asset-detail/{id}/')



# Delete Image 
@login_required
def delete_image(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        asset_obj = AssetMaster.objects.filter(pk=id).update( 
        image= None,
        )
        if asset_obj:

            return HttpResponse("success")
        return HttpResponse("failed")



#Clone Asset
@login_required
def clone_asset(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        asset_obj = AssetMaster.objects.get(pk=id)
        if asset_obj:
            AssetMaster.objects.create(
            area= asset_obj.area,
            image= asset_obj.image,
            fc_no= asset_obj.fc_no,
            category= asset_obj.category,
            description="clone_of_id_"+ str(asset_obj.id)+"_"+ asset_obj.description,
            brand= asset_obj.brand,
            model_no= asset_obj.model_no,
            serial_no= asset_obj.serial_no,
            sku= asset_obj.sku,
            asset_tag= asset_obj.asset_tag,
            status= asset_obj.status,
            age= asset_obj.age,
            upcoming_service_date= asset_obj.upcoming_service_date,
            last_service_date= asset_obj.last_service_date,

            #Unit of measurement
            length=asset_obj.length,
            breadth=asset_obj.breadth,
            width=asset_obj.width,
            height=asset_obj.height,

            #Product Engineering Support Info
            warranty_period=asset_obj.warranty_period,
            under_amc=asset_obj.under_amc,
            amc_date=asset_obj.amc_date,

            #Asset In and Out Tracking
            storage_warehouse_number=asset_obj.storage_warehouse_number,
            availability=asset_obj.availability,
            outward_date=asset_obj.outward_date,
            outward_remarks=asset_obj.outward_remarks,
            inward_date=asset_obj.inward_date,
            inward_remarks=asset_obj.inward_remarks,

            #Purchase
            vendor=asset_obj.vendor,
            purchased_on=asset_obj.purchased_on,
            cost_price=asset_obj.cost_price,
            tax_rate=asset_obj.tax_rate,
            depricated_value=asset_obj.depricated_value,
            created_on=asset_obj.created_on,

            #Pricing
            rental_pricing=asset_obj.rental_pricing,
            rent_collected=asset_obj.rent_collected,
            available_for_sale=asset_obj.available_for_sale,

            #Usage Information
            asset_utilization=asset_obj.asset_utilization,

            #Asset Status
            asset_status=asset_obj.asset_status,

            #Loan status
            loan_period=asset_obj.asset_status,
            loaned_asset=asset_obj.loaned_asset,


            #Sold Status
            sold_asset=asset_obj.sold_asset,

            rented_asset=asset_obj.rented_asset
            )
            return redirect('/asset-list/')
        return HttpResponse("failed")
        
        




# Asset List Class
# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
class AssetListView(ListAPIView, LoginRequiredMixin):
    login_url = "/login/"
    queryset = AssetMaster.objects.all()
    pagination_class = AssetMasterPagination
    template_name = 'assest_list.html'
    serializer_class = AssetMasterSerializer
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
            return AssetMaster.objects.filter(
                Q(brand__icontains=query) |
                Q(category__icontains=query) |
                Q(model_no__icontains=query) |
                Q(serial_no__icontains=query) |
                Q(description__icontains=query),
                sold_asset=False,
                rented_asset=False,
                loaned_asset=False,
            )
        elif query and filter_type=='category':
            return AssetMaster.objects.filter(category__icontains=query, sold_asset=False, rented_asset=False,
                loaned_asset=False)
        elif query and filter_type=='model_no':
            return AssetMaster.objects.filter(model_no__icontains=query, sold_asset=False, rented_asset=False,
                loaned_asset=False)
        elif query and filter_type=='brand':
            return AssetMaster.objects.filter(brand__icontains=query, sold_asset=False, rented_asset=False,
                loaned_asset=False)
        else:
            return AssetMaster.objects.filter(
                                              sold_asset=False,
                                              rented_asset=False,
                                              loaned_asset=False,
                                              )
            
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset(request).order_by('category').filter()
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
            {'assets': paginated_assets, 'queryset_length': queryset_length, **ctx}  # Merge assets and context data
        )






def autocomplete_search_group_wise(request):
    selected_value = request.GET.get('selected_value')
    if selected_value == 'category':
        total_assets = AssetMaster.objects.filter(relation=101).values_list('category', flat=True).distinct().order_by('category')
        return JsonResponse(list(total_assets), safe=False)
    
    elif selected_value == 'model_no':
        total_assets = AssetMaster.objects.filter(relation=101).values_list('model_no', flat=True).distinct().order_by('model_no')
        return JsonResponse(list(total_assets), safe=False)

    elif selected_value == 'brand':
        total_assets = AssetMaster.objects.filter(relation=101).values_list('brand', flat=True).distinct().order_by('brand')
        return JsonResponse(list(total_assets), safe=False)
    
    elif selected_value == 'description':
        total_assets = AssetMaster.objects.filter(relation=101).values_list('description', flat=True).distinct().order_by('brand')
        return JsonResponse(list(total_assets), safe=False)
  
    else:
        return JsonResponse([], safe=False)




#Asset list grouping
def group_wise_asset_list(request):

    ctx={}
    query = None
    query_params_q = None
    query_params_filter_value = None
    queryset_length = None


    if request.GET.get('q') is not None:
        query = request.GET.get('q').strip()
    
    if request.GET.get('q') is not None:
        query_params_q = request.GET.get('q').strip()
    
    if request.GET.get('filter_type'):
        query_params_filter_value = request.GET.get('filter_type').strip() or None

    if request.GET.get('q') and request.GET.get('filter_type') == 'category':
        # query = request.GET.get('q')
        asset_obj = list(AssetMaster.objects.filter(relation=101, 
                                                    category__iexact=query,
                                                    sold_asset=False
                                                    )
                                    .values('id','category','description','serial_no', 'model_no', 'brand'))
        
        new_asset_obj = list(map(lambda x: {**x, 'unique_asset': x['category'] + "-" + x['serial_no']}, asset_obj))

        asset_acc_obj = list(AssetMaster.objects.filter(relation=102,sold_asset=False)
                                 .values('id','category','description',
                                          'serial_no', 'model_no', 'brand', 'mapping'))
        
        queryset_length = len(asset_obj)
    
    
    elif request.GET.get('q') and request.GET.get('filter_type') == 'brand':
        # query = request.GET.get('q')
        asset_obj = list(AssetMaster.objects.filter(relation=101,
                                                    brand__iexact=query,
                                                    sold_asset=False)
                                    .values('id','category','description','serial_no', 'model_no', 'brand'))
        

        asset_acc_obj = list(AssetMaster.objects.filter(relation=102, sold_asset=False)
                                 .values('id','category','description',
                                          'serial_no', 'model_no', 'brand', 'mapping'))
        
        queryset_length = len(asset_obj)
    
    
    elif request.GET.get('q') and request.GET.get('filter_type') == 'model_no':
        # query = request.GET.get('q')
        asset_obj = list(AssetMaster.objects.filter(relation=101,
                                                    model_no__iexact=query,
                                                    sold_asset=False)
                                    .values('id','category','description','serial_no', 'model_no', 'brand'))
        

        asset_acc_obj = list(AssetMaster.objects.filter(relation=102, sold_asset=False)
                                 .values('id','category','description',
                                          'serial_no', 'model_no', 'brand', 'mapping'))
        
        queryset_length = len(asset_obj)
    
    
    elif request.GET.get('q') and request.GET.get('filter_type') == 'description':
        # query = request.GET.get('q')
        asset_obj = list(AssetMaster.objects.filter(relation=101,
                                                    description__iexact=query,
                                                    sold_asset=False)
                                    .values('id','category','description','serial_no', 'model_no', 'brand'))
        

        asset_acc_obj = list(AssetMaster.objects.filter(relation=102, sold_asset=False)
                                 .values('id','category','description',
                                          'serial_no', 'model_no', 'brand', 'mapping'))
        
        queryset_length = len(asset_obj)

    elif query and not request.GET.get('filter_type'):
        asset_obj = list(AssetMaster.objects.filter(
                Q(category__icontains=query) |
                Q(description__icontains=query),
                relation=101,
                sold_asset=False,
            ).values('id','category','description','serial_no', 'model_no', 'brand'))
        asset_acc_obj = list(AssetMaster.objects.filter(relation=102, sold_asset=False)
                                 .values('id','category','description',
                                          'serial_no', 'model_no', 'brand', 'mapping'))
        
        queryset_length = len(asset_obj)
    

    else:
        asset_obj = list(AssetMaster.objects.filter(relation=101, sold_asset=False)
                                    .values('id','category','description','serial_no',
                                             'model_no', 'brand'))
        
        asset_acc_obj = list(AssetMaster.objects.filter(relation=102, sold_asset=False)
                                        .values('id','category','description',
                                          'serial_no', 'model_no', 'brand', 'mapping'))
        
        queryset_length = len(asset_obj)
    
    # for asset in asset_obj:
    #     if 'asset_accessories' not in asset:
    #         asset['asset_accessories'] = []
    #         asset['asset_accessories_description'] = []
        
    #     for asset_acc in asset_acc_obj:
    #         if asset_acc['mapping'] == asset['description']:
    #             if (asset_acc['description']) not in asset['asset_accessories_description']: 
    #                 asset['asset_accessories_description'].append(asset_acc['description'])
    #                 asset['asset_accessories'].append({
    #                     'description': asset_acc['description'],
    #                     'id':asset_acc['id'],
    #                     'serial_no':asset_acc['serial_no'],
    #                     'model_no':asset_acc['model_no'],
    #                     'brand':asset_acc['brand']
    #                 })
    #                 asset_acc_obj.remove(asset_acc)
        
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



    paginator = Paginator(asset_obj, 10) 
    page = request.GET.get('page')

    try:
        asset_obj_paginated = paginator.page(page)
    except PageNotAnInteger:

        asset_obj_paginated = paginator.page(1)
    except EmptyPage:

        asset_obj_paginated = paginator.page(paginator.num_pages)

    ctx["asset_obj"] = asset_obj_paginated
    ctx["query_params_q"] = query_params_q
    ctx["query_params_filter_value"] = query_params_filter_value
    ctx["queryset_length"] = queryset_length
    
    return render(request, 'group_wise_asset_list.html', ctx)





#Select accessories group wise
class GetGroupWiseAssetAccessories(ListAPIView):
    pagination_class = AssetMasterPagination
    serializer_class = AssetMasterSerializer
    filter_backends = [filters.OrderingFilter]

    def list(self, request, *args, **kwargs):
        asset_id  = request.query_params.get('id') or request.session['asset_id']
        asset_obj = AssetMaster.objects.filter(id=asset_id).values('relation', 'description').first()
        if asset_obj is None :
            return Response({'error': 'Asset not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if asset_obj.get('relation') == 102:
            
            AssetMaster.objects.filter(pk=asset_id).update( 
            add_to_order = True,
            asset_status = "rented_out"
            )
            return Response({'rented_status': True})
        elif asset_obj.get('relation') == 101:
            asset_desc = asset_obj.get('description')

            AssetMaster.objects.filter(pk=asset_id).update( 
            add_to_order = True,
            asset_status = "rented_out"
            )

            search_field = None

            if request.query_params.get('search_field'):
                search_field = request.query_params.get('search_field')

            


            
            if request._request.GET.get('filter_value') and request._request.GET.get('filter_type'):
                filter_value = request._request.GET.get('filter_value')
                filter_type = request._request.GET.get('filter_type')
                if filter_type == 'model_no':
                    asset_acc_obj = list(AssetMaster.objects.filter(relation=102, sold_asset=False, 
                                                            mapping=asset_desc, model_no=filter_value)
                                        .values('id','category','description',
                                          'serial_no', 'model_no', 'brand', 'add_to_order',
                                           'mapping', 'owner', 'asset_status', 'confirm_order'))
                if filter_type == 'category':
                    asset_acc_obj = list(AssetMaster.objects.filter(relation=102, sold_asset=False, 
                                                            mapping=asset_desc,
                                                            category=filter_value)
                                        .values('id','category','description',
                                          'serial_no', 'model_no', 'brand', 'add_to_order',
                                           'mapping', 'owner', 'asset_status', 'confirm_order'))
                if filter_type == 'brand':
                    asset_acc_obj = list(AssetMaster.objects.filter(relation=102, sold_asset=False, 
                                                            mapping=asset_desc, 
                                                            brand=filter_value)
                                        .values('id','category','description',
                                          'serial_no', 'model_no', 'brand', 'add_to_order',
                                           'mapping', 'owner', 'asset_status', 'confirm_order'))
                    

            elif request._request.GET.get('filter_value') is None and search_field:
                
                asset_acc_obj = list(AssetMaster.objects.filter(
                Q(brand__icontains=search_field) |
                Q(category__icontains=search_field) |
                Q(model_no__icontains=search_field) |
                Q(serial_no__icontains=search_field) |
                Q(description__icontains=search_field),
                sold_asset=False,
                relation=102,
                mapping=asset_desc
            ).values('id','category','description',
                                          'serial_no', 'model_no', 'brand', 'add_to_order',
                                           'mapping', 'owner', 'asset_status', 'confirm_order'))
                    

            else:
                asset_acc_obj = list(AssetMaster.objects.filter(relation=102, sold_asset=False, 
                                                            mapping=asset_desc)
                                        .values('id','category','description',
                                          'serial_no', 'model_no', 'brand', 'add_to_order',
                                           'mapping', 'owner', 'asset_status', 'confirm_order'))
                        

            asset_obj_list = []

            while asset_acc_obj:
                new_array = []
                for m in asset_acc_obj:
                    get_description = m.get('description')
                    if get_description not in new_array:
                        new_array.append(get_description)
                        asset_obj_list.append(m)
                        asset_acc_obj.remove(m)
                    
            page = self.paginate_queryset(asset_obj_list)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(asset_obj_list, many=True)
            return Response(serializer.data)






class SoldAssetListView(ListAPIView, LoginRequiredMixin):
    queryset = AssetMaster.objects.all()
    pagination_class = AssetMasterPagination
    template_name = 'sold_list.html'
    serializer_class = AssetMasterSerializer
    filter_backends = [filters.OrderingFilter]
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    ordering = ["-id"]
    def get_queryset(self, request):
        query = None
        if self.request.GET.get('q') is not None:
            query = self.request.GET.get('q').strip()
        request.session['query'] = query
        if query:
            return AssetMaster.objects.filter(
                Q(area__icontains=query) |
                Q(asset_tag__icontains=query) |
                Q(brand__icontains=query) |
                Q(category__icontains=query) |
                Q(model_no__icontains=query) |
                Q(serial_no__icontains=query) |
                Q(sku__icontains=query) |
                Q(asset_tag__icontains=query) |
                Q(status__icontains=query), 
                sold_asset=True
            )
    
        else:
            return AssetMaster.objects.filter(sold_asset=True).order_by('id')
            
    
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
            {'assets': paginated_assets, 'queryset_length': queryset_length, **ctx}  # Merge assets and context data
        )




#Asset Detail View
@login_required
# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def asset_detail_view(request,id):
    ctx={}
    request.session['asset_id'] = id
    asset_obj=AssetMaster.objects.filter(id=id)
    if request.user.is_authenticated:
        asset_obj_files = AssetMasterAttachFile.objects.filter(asset_id=id)
        asset_obj_comment = AssetMasterComment.objects.filter(asset_id=id)
        customer = CustomerDetail.objects.all()
        ctx['comments'] = asset_obj_comment
        ctx['attached_files'] = asset_obj_files
        ctx['assets']=asset_obj
        ctx['customer']=customer
        ctx['user_email']=request.user.email

        return render(request,'asset_detail.html',ctx)
    else:
        ctx['assets']=asset_obj
        return render(request,'asset_detail.html',ctx)


#Set availability
@login_required
def set_availability(request):
    if request.method == 'POST':
        boolean_value = request.POST.get('boolean_field')
        id = request.POST.get('id')
        if boolean_value == '1':
            boolean_value = True
            AssetMaster.objects.filter(pk=id).update( 
            availability= boolean_value
        )
        else:
            boolean_value = False
            AssetMaster.objects.filter(pk=id).update( 
            availability= boolean_value)
    return render(request, 'asset_detail.html')


#Set under AMC
@login_required
def set_under_amc(request):
    if request.method == 'POST':
        boolean_value = request.POST.get('boolean_field')
        id = request.POST.get('id')
        if boolean_value == '1':
            boolean_value = True
            AssetMaster.objects.filter(pk=id).update( 
            under_amc= boolean_value
        )
        else:
            boolean_value = False
            AssetMaster.objects.filter(pk=id).update( 
            under_amc= boolean_value)
    return render(request, 'asset_detail.html')


#Set asset status
@login_required
def set_asset_status(request):
    if request.method == 'POST':
        asset_status = request.POST.get('set_asset_status')
        id = request.POST.get('id')
        if asset_status != 'available':
            availability=False
        else:
            availability=True
        AssetMaster.objects.filter(pk=id).update( 
            asset_status=asset_status,
            availability=availability
        )
    return render(request, 'asset_detail.html')



# Delete Asset View
class AssetMultipleDeleteView(APIView):
    def post(self, request):
        ids = request.data.getlist('id', []) 
        assets = AssetMaster.objects.filter(pk__in=ids)

        if not assets.exists():
            return Response("No assets found with given IDs.", status=status.HTTP_404_NOT_FOUND)

        assets.delete()
        messages.success(request, f"Asset with IDs {ids} deleted.")
        return redirect('/asset-list/')

    def get(self, request, id):
        asset = get_object_or_404(AssetMaster, pk=id)
        serial_no=asset.serial_no
        if asset:
            asset.delete()
            messages.success(request, f"Asset with Serial No.{serial_no} deleted.")
            return redirect('/asset-list/')
        else:
            return Response(f"Asset with ID {id} not found.", status=status.HTTP_404_NOT_FOUND)


# Delete Asset View
class SoldAssetMultipleDeleteView(APIView):
    def post(self, request):
        ids = request.data.getlist('id', []) 
        assets = AssetMaster.objects.filter(pk__in=ids)

        if not assets.exists():
            return Response("No assets found with given IDs.", status=status.HTTP_404_NOT_FOUND)

        assets.delete()
        messages.success(request, f"Asset with IDs {ids} deleted.")
        return redirect('/sold-list/')

    def get(self, request, id):
        asset = get_object_or_404(AssetMaster, pk=id)
        serial_no=asset.serial_no
        if asset:
            asset.delete()
            messages.success(request, f"Asset with Serial No.{serial_no} deleted.")
            return redirect('/sold-list/')
        else:
            return Response(f"Asset with ID {id} not found.", status=status.HTTP_404_NOT_FOUND)


# Delete Asset View
class LoanAssetMultipleDeleteView(APIView):
    def post(self, request):
        ids = request.data.getlist('id', []) 
        assets = AssetMaster.objects.filter(pk__in=ids)

        if not assets.exists():
            return Response("No assets found with given IDs.", status=status.HTTP_404_NOT_FOUND)

        assets.delete()
        messages.success(request, f"Asset with IDs {ids} deleted.")
        return redirect('/loan-list/')

    def get(self, request, id):
        asset = get_object_or_404(AssetMaster, pk=id)
        serial_no=asset.serial_no
        if asset:
            asset.delete()
            messages.success(request, f"Asset with Serial No.{serial_no} deleted.")
            return redirect('/loan-list/')
        else:
            return Response(f"Asset with ID {id} not found.", status=status.HTTP_404_NOT_FOUND)


# Delete Asset View
class RentAssetMultipleDeleteView(APIView):
    def post(self, request):
        ids = request.data.getlist('id', []) 
        assets = AssetMaster.objects.filter(pk__in=ids)

        if not assets.exists():
            return Response("No assets found with given IDs.", status=status.HTTP_404_NOT_FOUND)

        assets.delete()
        messages.success(request, f"Asset with IDs {ids} deleted.")
        return redirect('/rent-list/')

    def get(self, request, id):
        asset = get_object_or_404(AssetMaster, pk=id)
        serial_no=asset.serial_no
        if asset:
            asset.delete()
            messages.success(request, f"Asset with Serial No.{serial_no} deleted.")
            return redirect('/rent-list/')
        else:
            return Response(f"Asset with ID {id} not found.", status=status.HTTP_404_NOT_FOUND)



#Login View
def login_view(request):
    ctx={}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                ctx['user_email']=request.user.email
                return render(request, "qna_dashboard.html", ctx)
            else:
                return HttpResponse("Invalid Email or password")
        else:
            return HttpResponse("Invalid Email or password")

    else:
        return render(request, 'login.html')


#Logout View
def logout_view(request):
    logout(request)
    return redirect('/login/')


#Upload Excel
def upload_aaset_excel(request):
    print ("asset me jaa rha hun")
    try:
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
           

        for index, row in df.iterrows():
            # if row['RELATION'] == 101:
            asset = AssetMaster.objects.create(
                area=row['AREA'],
                fc_no=row['FC NO.'],
                category=row['CATEGORY'],
                description=row['DESCRIPTION'],
                sub_category=row['SUB CATEGORY'],
                brand=row['BRAND'],
                model_no=row['MODEL NO'],
                serial_no=row['SERIAL NO'],
                sku=row['SKU'],
                asset_tag=row['ASSET TAG'],
                status=row['STATUS'],
                mapping=row['MAPPING'],
                relation=row['RELATION'],
                box_number=row['BOX NO.'],
            )
            if row['RELATION'] == 102:
                asset = AssetMasterAccessories.objects.create(
                    area=row['AREA'],
                    fc_no=row['FC NO.'],
                    category=row['CATEGORY'],
                    description=row['DESCRIPTION'],
                    sub_category=row['SUB CATEGORY'],
                    brand=row['BRAND'],
                    model_no=row['MODEL NO'],
                    serial_no=row['SERIAL NO'],
                    sku=row['SKU'],
                    asset_tag=row['ASSET TAG'],
                    status=row['STATUS'],
                    mapping=row['MAPPING'],
                    relation=row['RELATION'],
                    box_number=row['BOX NO.'],                

                )
        messages.success(request, "File Uploaded")
        return redirect('/asset-list/')
    except Exception as e:
        messages.error(request, "This file is not supported")
        print(e, "-----------error---------------------------------")
        return redirect('/asset-list/')
    

#Import sold list
def upload_sold_aaset_excel(request):
    try:
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
           

        for index, row in df.iterrows():
            # if row['RELATION'] == 101:
            asset = AssetMaster.objects.create(
                area=row['AREA'],
                fc_no=row['FC NO.'],
                category=row['CATEGORY'],
                description=row['DESCRIPTION'],
                sub_category=row['SUB CATEGORY'],
                brand=row['BRAND'],
                model_no=row['MODEL NO'],
                serial_no=row['SERIAL NO'],
                sku=row['SKU'],
                asset_tag=row['ASSET TAG'],
                status=row['STATUS'],
                mapping=row['MAPPING'],
                relation=row['RELATION'],
                sold_asset=True
            )
        messages.success(request, "File Uploaded")
        return redirect('sold-list/')
    except:
        messages.error(request, "This file is not supported")
        return redirect('sold-list/')



#Import loan list
def upload_loan_aaset_excel(request):
    try:
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
           

        for index, row in df.iterrows():
            # if row['RELATION'] == 101:
            asset = AssetMaster.objects.create(
                area=row['AREA'],
                fc_no=row['FC NO.'],
                category=row['CATEGORY'],
                description=row['DESCRIPTION'],
                sub_category=row['SUB CATEGORY'],
                brand=row['BRAND'],
                model_no=row['MODEL NO'],
                serial_no=row['SERIAL NO'],
                sku=row['SKU'],
                asset_tag=row['ASSET TAG'],
                status=row['STATUS'],
                mapping=row['MAPPING'],
                relation=row['RELATION'],
                loaned_asset=True
            )
        messages.success(request, "File Uploaded")
        return redirect('loan-list/')
    except:
        messages.error(request, "This file is not supported")
        return redirect('loan-list/')


#Import loan list
def upload_rent_aaset_excel(request):
    try:
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
           

        for index, row in df.iterrows():
            # if row['RELATION'] == 101:
            asset = AssetMaster.objects.create(
                area=row['AREA'],
                fc_no=row['FC NO.'],
                category=row['CATEGORY'],
                description=row['DESCRIPTION'],
                sub_category=row['SUB CATEGORY'],
                brand=row['BRAND'],
                model_no=row['MODEL NO'],
                serial_no=row['SERIAL NO'],
                sku=row['SKU'],
                asset_tag=row['ASSET TAG'],
                status=row['STATUS'],
                mapping=row['MAPPING'],
                relation=row['RELATION'],
                rented_asset=True

            )
        messages.success(request, "File Uploaded")
        return redirect('loan-list/')
    except Exception as e:
        print(e,"-----------")
        messages.error(request, "This file is not supported")
        return redirect('loan-list/')




# def upload_excel_warehouse(request):
#     if request.method == 'POST':
#         form = ExcelUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             excel_file = request.FILES['excel_file']

#             if excel_file.name.endswith('.xlsx'):
#                 df = pd.read_excel(excel_file)
                
#                 for index, row in df.iterrows():
#                     serial_no = row['SERIAL NO']
#                     not_included_serial_no = []
#                     asset = AssetMaster.objects.filter(serial_no=serial_no).first()
#                     print(asset)
#                     if asset:                    
#                         Warehouse.objects.create(
#                         serial_no = asset,
#                         available=row['AVL'],
#                         outward_date=row['OUTWARD DATE'],
#                         inward_date=row['INWARD DATE'],
#                         inward=row['IN'],
#                         outward=row['OUT'],
#                         in_field=row['IN'],
#                         out_field=row['OUT'],
#                         remarks=row['REMARKS'],
#                         warehouse=row['WH'],    
#                     )
#                     else:
#                         not_included_serial_no.append(serial_no)
#                         print(not_included_serial_no,"not_included_serial_no")

#                 return render(request, 'success.html')
#             else:
#                 return render(request, 'upload_file.html', {'form': form, 'error_message': 'Please upload a valid Excel file (.xlsx)'})
#     else:
#         form = ExcelUploadForm()
#     return render(request, 'upload_warehouse_excel.html', {'form': form})


#Dashboard
@login_required
def home (request):
    ctx = {}
    if request.user.is_authenticated:
        ctx['user_email']=request.user.email
    return render(request,'qna_dashboard.html', ctx)





@login_required
def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    queryset = AssetMaster.objects.all()
    writer = csv.writer(response)
    writer.writerow(["Serial no", "Asset tag", "Brand", "Category", "Area", "Vintage",
                         "Description", "Last service date", "Model no", "Fc no",
                         "Upcoming service date"])
    for obj in queryset:
        writer.writerow([obj.serial_no, obj.asset_tag, obj.brand, obj.category, obj.area, obj.age,
                         obj.description, obj.last_service_date, obj.model_no, obj.fc_no,
                         obj.upcoming_service_date])  
    return response



@login_required
def generate_asset_pdf(request):
    buf = io.BytesIO()
    c =   canvas.Canvas(buf, pagesize=letter, bottomup=0)
    text_obj = c.beginText()
    text_obj.setTextOrigin(inch, inch)
    text_obj.setFont("Helvetica", 14)
    asset_obj = AssetMaster.objects.get(pk=request.GET.get('id'))

    lines=[]
    lines.append(asset_obj.description)
    lines.append(asset_obj.serial_no)
    lines.append(asset_obj.brand)
    lines.append(asset_obj.category)
    lines.append(asset_obj.area)
    lines.append(asset_obj.age)
    lines.append(asset_obj.model_no)
    lines.append(asset_obj.status)
    # lines.append(asset_obj.last_service_date)
    # lines.append(asset_obj.upcoming_service_date)

    for line in lines:
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.showPage()
    c.save()
    buf.seek(0)
    
    return FileResponse(buf, as_attachment=True, filename='ron.pdf')


# Attach file to asset master...
@login_required
def attach_file_to_asset(request):
    fss=FileSystemStorage()        
    file = request.FILES['file']
    id = request.POST['id']
    removed_space_file_name = (file.name).replace(" ", "_")
    files = fss.save(removed_space_file_name, file)
    fileurl = fss.url(files)  
    fileurl=fileurl.lstrip("/")
    fileurl= fileurl.replace("media/","").replace(" ","_")
    asset_obj = AssetMaster.objects.filter(id=id).first()
    asset_file_obj = AssetMasterAttachFile.objects.create( 
        asset_id=asset_obj,
        attached_file=fileurl
        )
    messages.success(request, "New file attached")
    return redirect('/asset-detail/')


def rented(request, id):
    ctx={}
    asset_obj=AssetMaster.objects.filter(id=id)
    asset_obj_comment = AssetMasterComment.objects.filter(asset_id=id)
    asset_obj_files = AssetMasterAttachFile.objects.filter(asset_id=id)
    ctx['comments'] = asset_obj_comment
    ctx['assets']=asset_obj
    ctx['attached_files'] = asset_obj_files

    return render(request,"rented.html", ctx)


class OutsourceView(ListAPIView):
    queryset = AssetMaster.objects.all()
    pagination_class = AssetMasterPagination
    template_name = 'outsource.html'
    serializer_class = AssetMasterSerializer
    filter_backends = [filters.OrderingFilter]
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    ordering = ["-id"]
    def get_queryset(self, request):
        query = self.request.GET.get('q')
        request.session['query'] = query
        if query:
            return AssetMaster.objects.filter(
                Q(area__icontains=query) |
                Q(asset_tag__icontains=query) |
                Q(brand__icontains=query) |
                Q(category__icontains=query) |
                Q(model_no__icontains=query) |
                Q(serial_no__icontains=query) |
                Q(sku__icontains=query) |
                Q(asset_tag__icontains=query) |
                Q(status__icontains=query) 
                # Q(id=query)
            )
        else:
            return AssetMaster.objects.all().order_by('id')
            
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(request))
        queryset_length = len(queryset)
        query_params = request.query_params.get('q')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data, queryset_length, query_params, request)

    def get_paginated_response(self, data, queryset_length, query_params, request):
        ctx = {}
        current_user = self.request.user
        if request.user.is_authenticated:
            ctx = {'user_email': current_user.email, "query_params": query_params} 
        paginated_assets = self.paginator.page if hasattr(self, 'paginator') else None
        return render(
            self.request,
            self.template_name,
            {'assets': paginated_assets, 'queryset_length': queryset_length, **ctx}  # Merge assets and context data
        )
    



# Delete attached file...
def delete_attached_file(request):
    if request.method == 'POST':
        asset_id=int(request.POST.get('asset_id'))
        id=request.POST.get('id')
        AssetMasterAttachFile.objects.get(pk=id).delete()
        messages.success(request, "File deleted")
    return HttpResponse("failed")






# Outsource
def update_comment_again_outsource(request):
    id = request.POST.get('id')
    ctx={}
    asset_obj = AssetMasterComment.objects.create(
        date_time = datetime.datetime.now(),
        asset_id = id,
        comment = request.POST.get('comment')
        )
    
    return redirect(f'/asset-management-rented/{id}/')



def attach_file_to_asset_outsource(request):
    fss=FileSystemStorage()        
    file = request.FILES['file']
    id = request.POST['id']
    removed_space_file_name = (file.name).replace(" ", "_")
    files = fss.save(removed_space_file_name, file)
    fileurl = fss.url(files)  
    fileurl=fileurl.lstrip("/")
    fileurl= fileurl.replace("media/","").replace(" ","_")
    asset_obj = AssetMaster.objects.filter(id=id).first()
    asset_file_obj = AssetMasterAttachFile.objects.create( 
        asset_id=asset_obj,
        attached_file=fileurl
        )
    messages.success(request, "New file attached")
    return redirect('/asset-management-rented/')



def delete_attached_file_outsource(request):
    if request.method == 'POST':
        asset_id=int(request.POST.get('asset_id'))
        id=request.POST.get('id')
        AssetMasterAttachFile.objects.get(pk=id).delete()
        messages.success(request, "File deleted")
    return HttpResponse("failed")

# def outsource_form(request):
#         return render(request,'outsource_form.html')


class AssetMasterOutsourcePostView(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        ctx = {}
        if request.user.is_authenticated:
            ctx['user_email']=request.user.email
        return render(request,'loan_form.html', ctx)


    def post(self, request):
        ctx = {}
        ctx['user_email']=request.user.email
        form_data = request.data
        serializer = AssetMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "New Asset added.")
            return redirect('/asset-management-outsource/')
        else:
            # messages.add_message(request, f'{serializer.error_messages['required']}')
            ctx['form_data'] = form_data
            return render(request, 'loan_form.html', ctx)
        


class AssetMultipleOutsourceDeleteView(APIView):
    def post(self, request):
        ids = request.data.getlist('id', []) 
        assets = AssetMaster.objects.filter(pk__in=ids)

        if not assets.exists():
            return Response("No assets found with given IDs.", status=status.HTTP_404_NOT_FOUND)

        assets.delete()
        messages.success(request, f"Asset with IDs {ids} deleted.")
        return redirect('/asset-management-outsource/')

    def get(self, request, id):
        asset = get_object_or_404(AssetMaster, pk=id)
        serial_no=asset.serial_no
        if asset:
            asset.delete()
            messages.success(request, f"Asset with Serial No.{serial_no} deleted.")
            return redirect('/asset-management-outsource/')
        else:
            return Response(f"Asset with ID {id} not found.", status=status.HTTP_404_NOT_FOUND)
        


def sold_detail(request, id):
    ctx={}
    asset_obj=AssetMaster.objects.filter(id=id)
    if request.user.is_authenticated:
        asset_obj_files = AssetMasterAttachFile.objects.filter(asset_id=id)
        asset_obj_comment = AssetMasterComment.objects.filter(asset_id=id)
        ctx['comments'] = asset_obj_comment
        ctx['attached_files'] = asset_obj_files
        ctx['assets']=asset_obj
        ctx['user_email']=request.user.email

        return render(request,'sold_detail.html',ctx)
    else:
        ctx['assets']=asset_obj
        return render(request,'sold_detail.html', ctx)




def rent_detail(request, id):
        ctx={}
        asset_obj=AssetMaster.objects.filter(id=id)
        if request.user.is_authenticated:
            asset_obj_files = AssetMasterAttachFile.objects.filter(asset_id=id)
            asset_obj_comment = AssetMasterComment.objects.filter(asset_id=id)
            ctx['comments'] = asset_obj_comment
            ctx['attached_files'] = asset_obj_files
            ctx['assets']=asset_obj
            ctx['user_email']=request.user.email

            return render(request,'rent_detail.html',ctx)
        else:
            ctx['assets']=asset_obj
            return render(request,'rent_detail.html', ctx)

class LoanListView(ListAPIView):
    queryset = AssetMaster.objects.all()
    pagination_class = AssetMasterPagination
    template_name = 'loan_list.html'
    serializer_class = AssetMasterSerializer
    filter_backends = [filters.OrderingFilter]
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    ordering = ["-id"]
    def get_queryset(self, request):
        query = self.request.GET.get('q')
        request.session['query'] = query
        if query:
            return AssetMaster.objects.filter(
                Q(area__icontains=query) |
                Q(asset_tag__icontains=query) |
                Q(brand__icontains=query) |
                Q(category__icontains=query) |
                Q(model_no__icontains=query) |
                Q(serial_no__icontains=query) |
                Q(sku__icontains=query) |
                Q(asset_tag__icontains=query) |
                Q(status__icontains=query), 
                loaned_asset=True,
                
            )
        else:
            return AssetMaster.objects.filter(loaned_asset=True, add_to_order=False).order_by('id')
            
    
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
            {'assets': paginated_assets, 'queryset_length': queryset_length, **ctx})
    


#Rent List view
class RentListView(ListAPIView):
    queryset = AssetMaster.objects.all()
    pagination_class = AssetMasterPagination
    template_name = 'rent_list.html'
    serializer_class = AssetMasterSerializer
    filter_backends = [filters.OrderingFilter]
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    ordering = ["-id"]
    def get_queryset(self, request):
        query = self.request.GET.get('q')
        request.session['query'] = query
        if query:
            return AssetMaster.objects.filter(
                Q(area__icontains=query) |
                Q(asset_tag__icontains=query) |
                Q(brand__icontains=query) |
                Q(category__icontains=query) |
                Q(model_no__icontains=query) |
                Q(serial_no__icontains=query) |
                Q(sku__icontains=query) |
                Q(asset_tag__icontains=query) |
                Q(status__icontains=query), 
                rented_asset=True,
                add_to_order=False
                
            )
        else:
            return AssetMaster.objects.filter(rented_asset=True, add_to_order=False).order_by('id')
            
    
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
            {'assets': paginated_assets, 'queryset_length': queryset_length, **ctx})


@login_required
def update_sold(request, id):
    ctx={}
    query=""
    asset_obj = AssetMaster.objects.filter(pk=id)
    serial_no = [asset.serial_no for asset in asset_obj]
    if request.user.is_authenticated:
        ctx['user_email']=request.user.email
    ctx['assets'] = asset_obj
    fss=FileSystemStorage()        
    if request.method == 'POST':
        model_no = request.POST.get('model_no')
        if request.FILES.get('image'):
            file = request.FILES.get('image')
            files = fss.save(file.name, file)
            fileurl = fss.url(files)  
            fileurl=fileurl.lstrip("/")
            fileurl= fileurl.replace("media/","")
        serial_no=request.POST.get('serial_no',None)
        category=request.POST.get('category',None)
        asset_tag=request.POST.get('asset_tag',None)
        brand=request.POST.get('brand',None)
        sku=request.POST.get('sku',None)
        fc_no=request.POST.get('fc_no',None)
        description=request.POST.get('description',None)
        status=request.POST.get('status',None)
        age=request.POST.get('age',None) 
        box_number=request.POST.get('box_number',None) 
        last_service_date=request.POST.get('last_service_date') or None
        upcoming_service_date=request.POST.get('upcoming_service_date') or None

        #Unit of measurement
        length=request.POST.get('length',None) 
        breadth=request.POST.get('breadth',None)
        width=request.POST.get('width',None) 
        height=request.POST.get('height',None)

        #Product Engineering Support Info
        warranty_period=request.POST.get('warranty_period',None)
        amc_date=request.POST.get('amc_date') or None

        #Asset In and Out Tracking
        storage_warehouse_number=request.POST.get('storage_warehouse_number',None)
        outward_date=request.POST.get('outward_date') or None
        outward_remarks=request.POST.get('outward_remarks',None)
        inward_date=request.POST.get('inward_date') or None
        inward_remarks=request.POST.get('inward_remarks',None)

        #Purchase
        vendor=request.POST.get('vendor',None)
        purchased_on=request.POST.get('purchased_on') or None
        cost_price=request.POST.get('cost_price',None)
        tax_rate=request.POST.get('tax_rate',None)
        depricated_value=request.POST.get('depricated_value',None)
        created_on=request.POST.get('created_on') or None

        #Pricing
        rental_pricing=request.POST.get('rental_pricing',None)
        rent_collected=request.POST.get('rent_collected',None)
        available_for_sale=request.POST.get('available_for_sale',None)

        #Usage Information
        asset_utilization=request.POST.get('asset_utilization',None)

        #Asset status
        # asset_status=request.POST.get('asset_status',None)

        

        if request.FILES.get('image'):
            asset_obj.update( 
            image=fileurl,
            model_no=model_no,
            serial_no=serial_no,
            category = category,
            asset_tag = asset_tag,
            brand = brand,
            sku = sku,
            fc_no = fc_no,
            description = description,
            status = status,
            age = age,
            box_number = box_number,
            last_service_date = last_service_date,
            upcoming_service_date = upcoming_service_date,

            #Unit of measurement
            length=length,
            breadth=breadth,
            width=width,
            height=height,
            warranty_period=warranty_period,
            storage_warehouse_number=storage_warehouse_number,
            outward_date=outward_date,
            outward_remarks=outward_remarks,
            inward_date=inward_date,
            inward_remarks=inward_remarks,
            vendor=vendor,
            purchased_on=purchased_on,
            cost_price=cost_price,
            tax_rate=tax_rate,
            depricated_value=depricated_value,
            created_on=created_on,
            rental_pricing=rental_pricing,
            rent_collected=rent_collected,
            available_for_sale=available_for_sale,
            asset_utilization=asset_utilization,

            )
        else:
            asset_obj.update(
            model_no=model_no,
            serial_no=serial_no,
            category = category,
            asset_tag = asset_tag,
            brand = brand,
            sku = sku,
            fc_no = fc_no,
            description = description,
            status = status,
            age = age,
            box_number = box_number,
            last_service_date = last_service_date,
            upcoming_service_date = upcoming_service_date,

            #Unit of measurement
            length=length,
            breadth=breadth,
            width=width,
            height=height,

            #Product Engineering Support Info
            warranty_period=warranty_period,
            amc_date=amc_date,

            #Asset In and Out Tracking
            storage_warehouse_number=storage_warehouse_number,
            outward_date=outward_date,
            outward_remarks=outward_remarks,
            inward_date=inward_date,
            inward_remarks=inward_remarks,

            #Purchase
            vendor=vendor,
            purchased_on=purchased_on,
            cost_price=cost_price,
            tax_rate=tax_rate,
            depricated_value=depricated_value,
            created_on=created_on,

            #Pricing
            rental_pricing=rental_pricing,
            rent_collected=rent_collected,
            available_for_sale=available_for_sale,

            #Usage Information
            asset_utilization=asset_utilization,
            )    
        if request.session['query'] and not request.session['filter_type']:
            query=request.session['query']   
            messages.success(request, f"Asset details with Serial No.{serial_no} updated.")
            return redirect(f'/sold-list/?q={query}')
        messages.success(request, f"Asset details with Serial No.{serial_no} updated.")
        # del request.session['query']
        return redirect(f'/sold-detail/{id}/')       
    else:
        return render(request, 'edit_sold_asset_detail.html', ctx)




@login_required
def update_loaned_asset(request, id):
    ctx={}
    query=""
    asset_obj = AssetMaster.objects.filter(pk=id)
    serial_no = [asset.serial_no for asset in asset_obj]
    if request.user.is_authenticated:
        ctx['user_email']=request.user.email
    ctx['assets'] = asset_obj
    fss=FileSystemStorage()        
    if request.method == 'POST':
        model_no = request.POST.get('model_no')
        if request.FILES.get('image'):
            file = request.FILES.get('image')
            files = fss.save(file.name, file)
            fileurl = fss.url(files)  
            fileurl=fileurl.lstrip("/")
            fileurl= fileurl.replace("media/","")
        serial_no=request.POST.get('serial_no',None)
        category=request.POST.get('category',None)
        asset_tag=request.POST.get('asset_tag',None)
        brand=request.POST.get('brand',None)
        sku=request.POST.get('sku',None)
        fc_no=request.POST.get('fc_no',None)
        description=request.POST.get('description',None)
        status=request.POST.get('status',None)
        age=request.POST.get('age',None) 
        box_number=request.POST.get('box_number',None) 
        last_service_date=request.POST.get('last_service_date') or None
        upcoming_service_date=request.POST.get('upcoming_service_date') or None

        #Unit of measurement
        length=request.POST.get('length',None) 
        breadth=request.POST.get('breadth',None)
        width=request.POST.get('width',None) 
        height=request.POST.get('height',None)

        #Product Engineering Support Info
        warranty_period=request.POST.get('warranty_period',None)
        amc_date=request.POST.get('amc_date') or None

        #Asset In and Out Tracking
        storage_warehouse_number=request.POST.get('storage_warehouse_number',None)
        outward_date=request.POST.get('outward_date') or None
        outward_remarks=request.POST.get('outward_remarks',None)
        inward_date=request.POST.get('inward_date') or None
        inward_remarks=request.POST.get('inward_remarks',None)

        #Purchase
        vendor=request.POST.get('vendor',None)
        purchased_on=request.POST.get('purchased_on') or None
        cost_price=request.POST.get('cost_price',None)
        tax_rate=request.POST.get('tax_rate',None)
        depricated_value=request.POST.get('depricated_value',None)
        created_on=request.POST.get('created_on') or None

        #Pricing
        rental_pricing=request.POST.get('rental_pricing',None)
        rent_collected=request.POST.get('rent_collected',None)
        available_for_sale=request.POST.get('available_for_sale',None)

        #Usage Information
        asset_utilization=request.POST.get('asset_utilization',None)

        #Asset status
        # asset_status=request.POST.get('asset_status',None)

        #Loaned Assets
        loan_period=request.POST.get('loan_period',None)

        

        if request.FILES.get('image'):
            asset_obj.update( 
            image=fileurl,
            model_no=model_no,
            serial_no=serial_no,
            category = category,
            asset_tag = asset_tag,
            brand = brand,
            sku = sku,
            fc_no = fc_no,
            description = description,
            status = status,
            age = age,
            box_number = box_number,
            last_service_date = last_service_date,
            upcoming_service_date = upcoming_service_date,

            #Unit of measurement
            length=length,
            breadth=breadth,
            width=width,
            height=height,
            warranty_period=warranty_period,
            storage_warehouse_number=storage_warehouse_number,
            outward_date=outward_date,
            outward_remarks=outward_remarks,
            inward_date=inward_date,
            inward_remarks=inward_remarks,
            vendor=vendor,
            purchased_on=purchased_on,
            cost_price=cost_price,
            tax_rate=tax_rate,
            depricated_value=depricated_value,
            created_on=created_on,
            rental_pricing=rental_pricing,
            rent_collected=rent_collected,
            available_for_sale=available_for_sale,
            asset_utilization=asset_utilization,
            loan_period=loan_period,

            )
        else:
            asset_obj.update(
            model_no=model_no,
            serial_no=serial_no,
            category = category,
            asset_tag = asset_tag,
            brand = brand,
            sku = sku,
            fc_no = fc_no,
            description = description,
            status = status,
            age = age,
            box_number = box_number,
            last_service_date = last_service_date,
            upcoming_service_date = upcoming_service_date,

            #Unit of measurement
            length=length,
            breadth=breadth,
            width=width,
            height=height,

            #Product Engineering Support Info
            warranty_period=warranty_period,
            amc_date=amc_date,

            #Asset In and Out Tracking
            storage_warehouse_number=storage_warehouse_number,
            outward_date=outward_date,
            outward_remarks=outward_remarks,
            inward_date=inward_date,
            inward_remarks=inward_remarks,

            #Purchase
            vendor=vendor,
            purchased_on=purchased_on,
            cost_price=cost_price,
            tax_rate=tax_rate,
            depricated_value=depricated_value,
            created_on=created_on,

            #Pricing
            rental_pricing=rental_pricing,
            rent_collected=rent_collected,
            available_for_sale=available_for_sale,

            #Usage Information
            asset_utilization=asset_utilization,

            #Loaned Assets
            loan_period=loan_period,
            )    
        if request.session['query'] and not request.session['filter_type']:
            query=request.session['query']   
            messages.success(request, f"Asset details with Serial No.{serial_no} updated.")
            return redirect(f'/loan-list/?q={query}')
        messages.success(request, f"Asset details with Serial No.{serial_no} updated.")
        # del request.session['query']
        return redirect(f'/loan-detail/{id}/')       
    else:
        return render(request, 'edit_loan_detail.html', ctx)
    


@login_required
def update_rented_asset(request, id):
    ctx={}
    query=""
    asset_obj = AssetMaster.objects.filter(pk=id)
    serial_no = [asset.serial_no for asset in asset_obj]
    if request.user.is_authenticated:
        ctx['user_email']=request.user.email
    ctx['assets'] = asset_obj
    fss=FileSystemStorage()        
    if request.method == 'POST':
        model_no = request.POST.get('model_no')
        if request.FILES.get('image'):
            file = request.FILES.get('image')
            files = fss.save(file.name, file)
            fileurl = fss.url(files)  
            fileurl=fileurl.lstrip("/")
            fileurl= fileurl.replace("media/","")
        serial_no=request.POST.get('serial_no',None)
        category=request.POST.get('category',None)
        asset_tag=request.POST.get('asset_tag',None)
        brand=request.POST.get('brand',None)
        sku=request.POST.get('sku',None)
        fc_no=request.POST.get('fc_no',None)
        description=request.POST.get('description',None)
        status=request.POST.get('status',None)
        age=request.POST.get('age',None) 
        box_number=request.POST.get('box_number',None) 
        last_service_date=request.POST.get('last_service_date') or None
        upcoming_service_date=request.POST.get('upcoming_service_date') or None

        #Unit of measurement
        length=request.POST.get('length',None) 
        breadth=request.POST.get('breadth',None)
        width=request.POST.get('width',None) 
        height=request.POST.get('height',None)

        #Product Engineering Support Info
        warranty_period=request.POST.get('warranty_period',None)
        amc_date=request.POST.get('amc_date') or None

        #Asset In and Out Tracking
        storage_warehouse_number=request.POST.get('storage_warehouse_number',None)
        outward_date=request.POST.get('outward_date') or None
        outward_remarks=request.POST.get('outward_remarks',None)
        inward_date=request.POST.get('inward_date') or None
        inward_remarks=request.POST.get('inward_remarks',None)

        #Purchase
        vendor=request.POST.get('vendor',None)
        purchased_on=request.POST.get('purchased_on') or None
        cost_price=request.POST.get('cost_price',None)
        tax_rate=request.POST.get('tax_rate',None)
        depricated_value=request.POST.get('depricated_value',None)
        created_on=request.POST.get('created_on') or None

        #Pricing
        rental_pricing=request.POST.get('rental_pricing',None)
        rent_collected=request.POST.get('rent_collected',None)
        available_for_sale=request.POST.get('available_for_sale',None)

        #Usage Information
        asset_utilization=request.POST.get('asset_utilization',None)

        #Asset status
        # asset_status=request.POST.get('asset_status',None)

        

        if request.FILES.get('image'):
            asset_obj.update( 
            image=fileurl,
            model_no=model_no,
            serial_no=serial_no,
            category = category,
            asset_tag = asset_tag,
            brand = brand,
            sku = sku,
            fc_no = fc_no,
            description = description,
            status = status,
            age = age,
            box_number = box_number,
            last_service_date = last_service_date,
            upcoming_service_date = upcoming_service_date,

            #Unit of measurement
            length=length,
            breadth=breadth,
            width=width,
            height=height,
            warranty_period=warranty_period,
            storage_warehouse_number=storage_warehouse_number,
            outward_date=outward_date,
            outward_remarks=outward_remarks,
            inward_date=inward_date,
            inward_remarks=inward_remarks,
            vendor=vendor,
            purchased_on=purchased_on,
            cost_price=cost_price,
            tax_rate=tax_rate,
            depricated_value=depricated_value,
            created_on=created_on,
            rental_pricing=rental_pricing,
            rent_collected=rent_collected,
            available_for_sale=available_for_sale,
            asset_utilization=asset_utilization,

            )
        else:
            asset_obj.update(
            model_no=model_no,
            serial_no=serial_no,
            category = category,
            asset_tag = asset_tag,
            brand = brand,
            sku = sku,
            fc_no = fc_no,
            description = description,
            status = status,
            age = age,
            box_number = box_number,
            last_service_date = last_service_date,
            upcoming_service_date = upcoming_service_date,

            #Unit of measurement
            length=length,
            breadth=breadth,
            width=width,
            height=height,

            #Product Engineering Support Info
            warranty_period=warranty_period,
            amc_date=amc_date,

            #Asset In and Out Tracking
            storage_warehouse_number=storage_warehouse_number,
            outward_date=outward_date,
            outward_remarks=outward_remarks,
            inward_date=inward_date,
            inward_remarks=inward_remarks,

            #Purchase
            vendor=vendor,
            purchased_on=purchased_on,
            cost_price=cost_price,
            tax_rate=tax_rate,
            depricated_value=depricated_value,
            created_on=created_on,

            #Pricing
            rental_pricing=rental_pricing,
            rent_collected=rent_collected,
            available_for_sale=available_for_sale,

            #Usage Information
            asset_utilization=asset_utilization,
            )    
        if request.session['query'] and not request.session['filter_type']:
            query=request.session['query']   
            messages.success(request, f"Asset details with Serial No.{serial_no} updated.")
            return redirect(f'/rent-list/?q={query}')
        messages.success(request, f"Asset details with Serial No.{serial_no} updated.")
        # del request.session['query']
        return redirect(f'/rent-detail/{id}/')       
    else:
        return render(request, 'edit_rent_detail.html', ctx)





def loan_detail(request, id):
    ctx={}
    asset_obj=AssetMaster.objects.filter(id=id)
    if request.user.is_authenticated:
        asset_obj_files = AssetMasterAttachFile.objects.filter(asset_id=id)
        asset_obj_comment = AssetMasterComment.objects.filter(asset_id=id)
        ctx['comments'] = asset_obj_comment
        ctx['attached_files'] = asset_obj_files
        ctx['assets']=asset_obj
        ctx['user_email']=request.user.email

        return render(request,'loan_detail.html',ctx)
    else:
        ctx['assets']=asset_obj
        return render(request,'loan_detail.html', ctx)



class AssetMasterLoanPostView(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        ctx = {}

        
        loaned_asset = list(AssetMaster.objects.filter(loaned_asset=True, relation=101).values_list('description').distinct())
        loaned_asset_description = [item[0] for item in loaned_asset]        
        ctx['loaned_asset_description'] = loaned_asset_description
        return render(request,'loan_form.html', ctx)


    def post(self, request):
        ctx = {}
        form_data = request.data

        if 'relation' not in request.data:
            return HttpResponse("Please provide a value for the 'relation' field")
        elif request.data['relation'] == '102' and request.data['mapping'] == '': 
            return HttpResponse("Please select a mapping field")
        
        mutable_data = request.data.copy() if isinstance(request.data, QueryDict) else request.data.copy()
        mutable_data['loaned_asset'] = True
        serializer = AssetMasterSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "New Asset added.")
            return redirect('/loan-list/')
        else:
            # messages.add_message(request, f'{serializer.error_messages['required']}')
            ctx['form_data'] = form_data
            return render(request, 'loan_form.html', ctx)
        


class AssetMasterRentPostView(APIView):
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        ctx = {}

        rented_asset = list(AssetMaster.objects.filter(loaned_asset=True, relation=101).values_list('description').distinct())
        rented_asset_description = [item[0] for item in rented_asset]        
        ctx['rented_asset_description'] = rented_asset_description

        return render(request,'rent_form.html', ctx)


    def post(self, request):
        ctx = {}
        ctx['user_email']=request.user.email
        form_data = request.data

        if 'relation' not in request.data:
            return HttpResponse("Please provide a value for the 'relation' field")
        elif request.data['relation'] == '102' and request.data['mapping'] == '': 
            return HttpResponse("Please select a mapping field")
        
        mutable_data = request.data.copy() if isinstance(request.data, QueryDict) else request.data.copy()
        mutable_data['rented_asset'] = True
        serializer = AssetMasterSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "New Asset added.")
            return redirect('/rent-list/')
        else:
            # messages.add_message(request, f'{serializer.error_messages['required']}')
            ctx['form_data'] = form_data
            return render(request, 'rent_form.html', ctx)



#Analytics category list
def analytics_list(request):
    ctx={}
    availability_list = []
    out_list = []
    all_data = []
    page_number = request.GET.get('page', 1) 
    if request.GET.get('q') and request.GET.get('filter_type') == 'category':
        category=request.GET.get('q')
        categories_with_total_asset_count = AssetMaster.objects.filter(category__iexact=category).values('category').annotate(category_count=Count('category'))
    elif request.GET.get('q') and request.GET.get('filter_type') == 'brand':
        brand=request.GET.get('q')
        categories_with_total_asset_count = AssetMaster.objects.filter(brand__iexact=brand).values('category').annotate(category_count=Count('category'))
    elif request.GET.get('q') and request.GET.get('filter_type') == 'model_no':
        model_no=request.GET.get('q')
        categories_with_total_asset_count = AssetMaster.objects.filter(model_no__iexact=model_no).values('category').annotate(category_count=Count('category'))
    elif request.GET.get('q'):
        category=request.GET.get('q')
        categories_with_total_asset_count = AssetMaster.objects.filter(category__iexact=category).values('category').annotate(category_count=Count('category'))
    else:
        categories_with_total_asset_count = AssetMaster.objects.values('category').annotate(category_count=Count('category'))
    category_length = len(categories_with_total_asset_count)
    for i in categories_with_total_asset_count:
        categories_with_availability_count=AssetMaster.objects.filter(category=i['category'],asset_status='available').count()
        availability_dict = {'availability': categories_with_availability_count}
        availability_list.append(availability_dict)
        categories_with_out_count=AssetMaster.objects.filter(category=i['category'],asset_status__in =['rented_out','sent_for_repair']).count()
        out_dict = {'out': categories_with_out_count}
        out_list.append(out_dict)
    categories_with_total_asset_count_dict = list(categories_with_total_asset_count.values('category', 'category_count'))
    for i, j, k in  zip(categories_with_total_asset_count_dict, availability_list, out_list):
        all_data.append({**i, **j, **k})
        
    if request.GET.get('filter_type'):
        ctx['query_params_filter_value'] = request.GET.get('filter_type')
    if request.GET.get('q'):
        ctx['query_params_q'] = request.GET.get('q')

    #Pagination
    paginator = Paginator(all_data, 10) 
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    ctx['category_list'] = paginated_data
    ctx['category_length'] = category_length
    download_csv_param = request.GET.get('download_csv')
    if download_csv_param:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

        # Write data to CSV
        writer = csv.writer(response)
        writer.writerow(['Category', 'Category Count', 'Availability']) 
        for item in all_data:
            writer.writerow([item['category'], item['category_count'], item['availability']])

        return response
    return render(request, 'analytics_list.html', ctx)



#Each category brand
def analytics_category(request, category):
    ctx={}
    availability_list = []
    all_data = []
    brand_non_availability_list = []
    page_number = request.GET.get('page', 1) 
    request.session['category'] = category
    if request.GET.get('q'):
        brand=request.GET.get('q')
        category_brand = AssetMaster.objects.filter(category__iexact=category,brand=brand).values('brand').annotate(brand_count=Count('brand'))
    else:
        category_brand = AssetMaster.objects.filter(category__iexact=category).values('brand').annotate(brand_count=Count('brand'))
    brand_length = len(category_brand)
    for i in category_brand:
        brand_availability = AssetMaster.objects.filter(category__iexact=category, brand=i['brand'],asset_status='available').count()
        availability_list.append({'availability': brand_availability})
        brand_non_availability = AssetMaster.objects.filter(category=category, brand=i['brand'], asset_status__in =['rented_out','sent_for_repair']).count()
        brand_non_availability_list.append({'not_available': brand_non_availability})
    category_brand_list = list(category_brand.values('brand', 'brand_count'))
    for i, j, k in  zip(category_brand_list, availability_list, brand_non_availability_list):
        all_data.append({**i, **j, **k})


    if request.GET.get('filter_type'):
        ctx['query_params_filter_value'] = request.GET.get('filter_type')
    if request.GET.get('q'):
        ctx['query_params_q'] = request.GET.get('q')

    #Pagination
    paginator = Paginator(all_data, 10) 
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)
    ctx['category_brand'] = paginated_data
    ctx['category'] = category
    ctx['brand_length'] = brand_length

    download_csv_param = request.GET.get('download_csv')
    if download_csv_param:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

        # Write data to CSV
        writer = csv.writer(response)
        writer.writerow(['Brand', 'Brand Count', 'Availability']) 
        for item in all_data:
            writer.writerow([item['brand'], item['brand_count'], item['availability']])

        return response
    
    
    return render(request,'analytics_category.html',ctx)



#Each brand model no.
def analytics_brand(request, brand):
    ctx={}
    availability_list = []
    all_data = []
    model_non_availibility_list = []
    page_number = request.GET.get('page', 1) 
    category=request.session['category']
    brand_model_no = AssetMaster.objects.filter(category=category,brand=brand).values('model_no').annotate(model_count=Count('model_no'))
    brand_model_no_length = len(brand_model_no)
    for i in brand_model_no:
        model_availability = AssetMaster.objects.filter(category=category, brand=brand, model_no=i['model_no'], asset_status='available').count()
        availability_list.append({'availability': model_availability}) 
        model_non_availability = AssetMaster.objects.filter(category=category, brand=brand, model_no=i['model_no'], asset_status__in =['rented_out','sent_for_repair']).count()
        model_non_availibility_list.append({'model_non_available': model_non_availability})
    brand_model_list = list(brand_model_no.values('model_no', 'model_count'))
    for i, j, k in  zip(brand_model_list, availability_list, model_non_availibility_list):
        all_data.append({**i, **j, **k})

    if request.GET.get('filter_type'):
        ctx['query_params_filter_value'] = request.GET.get('filter_type')
    if request.GET.get('q'):
        ctx['query_params_q'] = request.GET.get('q')

    #Paginations
    paginator = Paginator(all_data, 10) 
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)
    ctx['brand_model_no'] = paginated_data
    ctx['brand'] = brand
    ctx['category'] = category
    ctx['brand_model_no_length'] = brand_model_no_length

    download_csv_param = request.GET.get('download_csv')
    if download_csv_param:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

        # Write data to CSV
        writer = csv.writer(response)
        writer.writerow(['Model No.', 'Model Count', 'Availability']) 
        for item in all_data:
            writer.writerow([item['model_no'], item['model_count'], item['availability']])

        return response
    return render(request,'analytics_brand.html',ctx)