from django.db import models
import datetime
from asset_master.models import *


# Create your models here.
class RequirementDetail(models.Model):
    
    class RelationshipType(models.IntegerChoices):
        PARENT = 101
        CHILD = 102
    
    r_customer = models.CharField(max_length=100, blank=True, null=True)
    r_order_startdate = models.DateField(null=True, blank=True)
    r_order_depdate = models.DateField(null=True, blank=True)
    r_order_enddate = models.DateField(null=True, blank=True)
    r_order_loc=models.CharField(max_length=100,blank=True, null=True)

    r_category = models.CharField(max_length=100, null=True, blank=True)
    r_subcategory = models.CharField(max_length=100, null=True, blank=True)
    r_description = models.CharField(max_length=100, null=True, blank=True)
    r_brand = models.CharField(max_length=100, null=True, blank=True)
    r_modelno = models.CharField(max_length=100, null=True, blank=True)
    r_serialno = models.CharField(max_length=100, null=True, blank=True)
    quantity=models.IntegerField( null=True, blank=True)

    relation = models.IntegerField(choices=RelationshipType.choices, default=RelationshipType.PARENT)
    mapping = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    asset_tag = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    fc_no = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    box_number = models.CharField(max_length=100, null=True, blank=True, default="")



