# from django.shortcuts import render
# from rest_framework.viewsets import ViewSet
# from warehouse.models import Warehouse
# from .serializers import WarehouseSerializer
# from .pagination import WarehousePagination
# from rest_framework.generics import ListAPIView
# from django.db.models import Q
# from rest_framework.generics import ListAPIView


# # Create your views here.
# class WarehouseListView(ListAPIView):
#     queryset = Warehouse.objects.all()
#     pagination_class = WarehousePagination
#     template_name = 'warehouse_list.html'
#     serializer_class = WarehouseSerializer
#     def get_queryset(self, request):
#         query = self.request.GET.get('q')
#         request.session['query'] = query
#         if query:
#             return Warehouse.objects.filter(
#                 Q(warehouse__icontains=query) |
#                 Q(remarks__icontains=query) |
#                 Q(serial_no__icontains=query) 
                
#             )
#         else:
#             return Warehouse.objects.all().order_by('id')
            
    
#     def get(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset(request))
#         queryset_length = len(queryset)
#         query_params = request.query_params.get('q')
#         page = self.paginate_queryset(queryset)
#         serializer = self.get_serializer(page, many=True)
#         return self.get_paginated_response(serializer.data, queryset_length, query_params, request)

#     def get_paginated_response(self, data, queryset_length, query_params, request):
#         ctx = {}
#         current_user = self.request.user
#         if request.user.is_authenticated:
#             ctx = {'user_email': current_user.email, "query_params": query_params} 
#         paginated_assets = self.paginator.page if hasattr(self, 'paginator') else None
#         return render(
#             self.request,
#             self.template_name,
#             {'assets': paginated_assets, 'queryset_length': queryset_length, **ctx}  # Merge assets and context data
#         )


# def warehouse_detail(request, id):
#     ctx={}
#     asset_obj=Warehouse.objects.filter(id=id)
#     if request.user.is_authenticated:
#         # asset_obj_files = AssetMasterAttachFile.objects.filter(asset_id=id)
#         # asset_obj_comment = AssetMasterComment.objects.filter(asset_id=id)
#         # ctx['comments'] = asset_obj_comment
#         # ctx['attached_files'] = asset_obj_files
#         ctx['assets']=asset_obj
#         # ctx['user_email']=request.user.email

#         return render(request,'warehouse_details.html',ctx)
#     else:
#         ctx['assets']=asset_obj
#         return render(request,'warehouse_details.html')
