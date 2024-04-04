from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib import messages
from .serializers import OrderDetailSerializer, CustomerDetailSerializer
from asset_master.serializers import *
import pandas as pd
from orders.pagination import OrderDetailPagination
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
from orders.models import *
from .models import RequirementDetail
from .forms import *

# Create your views here.
def requirement_report_main_page(request):
   ctx={}

   requirement = RequirementDetail.objects.values('id','r_customer',
    'r_order_startdate', 'r_order_enddate' )

   ctx['requirement']=requirement

   return render(request, 'requirement_report_main_page.html', ctx)

# requirement per customer
def requirement_per_customer(request,id):
    ctx = {}

    # Fetching the customer object by id
    customer_obj = RequirementDetail.objects.filter(id=id).first()

    # Fetching the second object by id
    second_order_obj = RequirementDetail.objects.filter(id=id).order_by('id').first()

    if second_order_obj:
        # Fetching all assets of the second order
        all_asset_of_an_order = RequirementDetail.objects.filter(id=second_order_obj.id).values(
            'r_category', 'r_subcategory', 'r_description', 
            'r_brand', 'r_modelno', 'r_serialno','quantity'
        )
    else:
        all_asset_of_an_order = []

    ctx['customer_obj'] = customer_obj
    ctx['all_asset_of_an_order'] = all_asset_of_an_order

    return render(request, 'requirement_per_customer.html', ctx)

    # ctx={}
    # customer_obj = RequirementDetail.objects.filter(id=id).first()
    # order_obj=OrderDetail.objects.filter(id=id)
    # all_asset_of_an_order = RequirementDetail.objects.filter(id=customer_obj.id).values('r_category','r_subcategory',
    #  'r_description','r_brand', 'r_modelno', 'r_serialno' )
    # ctx['customer_obj']=customer_obj
    # ctx['all_asset_of_an_order'] = all_asset_of_an_order
    # return render(request,'requirement_per_customer.html',ctx)

#create requirement asset form
def requirement_asset_form(request):
    ctx={}
    customer=CustomerDetail.objects.all()
    ctx['customer']=customer
    return render(request,'requirement_asset.html',ctx)

#save requirement form
def requirement_save_form(request):
    if request.method=='POST':
       customer=request.POST.get('customer')
       r_order_startdate=request.POST.get('out_date_and_time')
       r_order_depdate=request.POST.get('deployment_date')
       r_order_enddate=request.POST.get('return_date')
       r_order_loc=request.POST.get('location')
       
       r_category=request.POST.get('category')
       r_subcategory=request.POST.get('subcategory')
       r_description=request.POST.get('description') 
       r_modelno=request.POST.get('model_no')
       r_brand=request.POST.get('brand')
       r_serialno=request.POST.get('serial_no')
       quantity=request.POST.get( 'quantity')

       data=RequirementDetail(
               r_customer=customer,
               r_order_startdate=r_order_startdate,
               r_order_depdate=r_order_depdate,
               r_order_enddate=r_order_enddate,
               r_order_loc=r_order_loc,
               r_category=r_category,
               r_subcategory=r_subcategory,
               r_description=r_description,
               r_brand=r_brand,
               r_modelno=r_modelno,
               r_serialno=r_serialno,
               quantity=quantity,
           
       )
       data.save()
    return render(request,'requirement_asset.html')


#Confirmed order Export to CSV
@login_required
def requirement_export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    
    queryset = RequirementDetail.objects.all()
    writer = csv.writer(response)
    writer.writerow(["CATEGORY", "SUBCATEGORY", "DISCRIPTION","BRAND", "MODELNO","SERIALNO","QUANTITY"])
    for obj in queryset:
        writer.writerow([obj.r_category, obj.r_subcategory,  obj.r_description, obj.r_brand,obj.r_modelno,obj.r_serialno,obj.quantity])  
        
    return response
# import csv
def upload_requirement_excel(request):
    print("requiremnt me jaa rha hun")
    try:
        csv_file=request.FILES['csv_file']
        if csv_file.name.endswith('.csv'):
            df = pd.read_csv(csv_file)
        elif csv_file.name.endswith('.xlsx'):
            df = pd.read_excel(csv_file)
          
        for index,row in df.iterrows():
            asset=RequirementDetail.objects.create(
               r_category=row['CATEGORY'],
               r_subcategory=row['SUB CATEGORY'],
               r_description=row['DESCRIPTION'],
               r_brand=row['BRAND'],
               r_modelno=row['MODEL NO'],
               r_serialno=row['SERIAL NO'],
               relation = row['RELATION'],
               mapping = row['MAPPING'],
               sku =row['SKU'],
               asset_tag = row['ASSET TAG'],
               area = row['AREA'],
               fc_no = row['FC NO.'],
               status = row['STATUS'],
               box_number=row['BOX NO.']
            )
        print("uploaded")
        messages.success(request,"file uploaded")
        return  render (request,'requirement_report_main_page.html')
    except Exception as e:
        print(e,"----------------")
        messages.error(request,"this file is not supported")
        return render(request,"requirement_asset.html")














# class ConfirmOrderListView(ListAPIView, LoginRequiredMixin):
#     # pagination_class = OrderDetailPagination
#     template_name = 'requirement_report_main_page.html'
#     serializer_class = OrderDetailSerializer
#     filter_backends = [filters.OrderingFilter]
#     authentication_classes = [BasicAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticated]
#     ordering = ["id"]
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
#             return OrderDetail.objects.filter(
#                 Q(organization__icontains=query) |
#                 Q(prepared_by_name__icontains=query),
#             )
#         elif query and filter_type=='customer_id':
#             return OrderDetail.objects.filter(customer_id__customer__iexact=query)
#         # elif query and filter_type=='deployment_date':
#         #     return OrderDetail.objects.filter(model_no__iexact=query)
#         elif query and filter_type=='order_id':
#             return OrderDetail.objects.filter(id=query)
#         # elif query and filter_type=='return_date':
#         #     return OrderDetail.objects.filter(brand__iexact=query, sold_asset=False, rented_asset=False,
#         #         loaned_asset=False, add_to_order=True, confirm_order=False)
#         else:
#             return OrderDetail.objects.all()
            
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
#         paginated_assets = self.paginator if hasattr(self, 'paginator') else None
#         return render(
#             self.request,
#             self.template_name,
#             {'orders': paginated_assets, 'queryset_length': queryset_length, **ctx}  # Merge assets and context data
#         )
