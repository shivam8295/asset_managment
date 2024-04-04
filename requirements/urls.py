from django.urls import path, include
from requirements.views import *

urlpatterns = [
    
#main page()
path("requirement-report-main-page/",requirement_report_main_page, name= "requirement_report_main_page"),

#requirement per customer
path("requirement-per-customer/<int:id>/",requirement_per_customer, name= "requirement_per_customer"),

#requirement form
path("requirement-asset/",requirement_asset_form, name= "requirement_asset"),

#requirement form
path("save-requirement-form",requirement_save_form, name= "save-requirement-form"),




#export to csv
path("requirement-exposed-to-csv/",requirement_export_to_csv, name= "requirement_export_to_csv"),

#import  csv
path("upload_req/",upload_requirement_excel, name= "upload_req"),

]

