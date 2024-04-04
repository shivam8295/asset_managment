from django.db import models
from asset_master.models import AssetMaster 
import uuid
# from enums.order_status_enum import OrderStatus




class CustomerDetail(models.Model):
    customer = models.CharField(max_length=100, blank=True, null=True)
    completed_orders = models.CharField(max_length=100, blank=True, null=True)
    deployed_order = models.CharField(max_length=100, blank=True, null=True)
    taxed = models.CharField(max_length=100, blank=True, null=True)
    email_address = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    customer_revenue = models.CharField(max_length=100, blank=True, null=True)
    commercial_address = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField(null=True, blank=True, default=None)
    secondary_email = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)



class CustomerAttachFile(models.Model):
    customer_id = models.ForeignKey(CustomerDetail, on_delete= models.CASCADE)
    attached_file = models.FileField(upload_to="media/", default=None, null=True, blank=True)


class CustomerComment(models.Model):
    customer_id = models.ForeignKey(CustomerDetail, on_delete= models.CASCADE)
    comment = models.CharField(max_length=100, null=True, blank=True)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)

class OrderDetail(models.Model):
    class OrderStatus(models.IntegerChoices):
            BOOKED = 1,
            APPROVED = 2,
            CANCELLED = 3,
            DISPATCHED = 4,
    assets = models.ManyToManyField(AssetMaster, related_name='order_details', blank=True)
    # order_id = models.UUIDField(editable=False, default=uuid.uuid4)
    customer_id = models.ForeignKey(CustomerDetail, on_delete=models.SET_NULL, null=True)
    price = models.CharField(null=True, blank=True, max_length=50)
    # rent_out_date = models.DateField(null=True, blank=True)
    order_status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.BOOKED)   
    organization = models.CharField(max_length=100, blank=True, null=True)
    # quantity = models.PositiveIntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)
    customer = models.CharField(max_length=100, null=True, blank=True)
    deployment_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    name_of_consignee = models.CharField(max_length=100, blank=True, null=True)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    mode_of_dispatch = models.CharField(max_length=100, blank=True, null=True)
    transportation = models.CharField(max_length=100, blank=True, null=True)
    order_to = models.CharField(max_length=100, blank=True, null=True)
    order_from = models.CharField(max_length=100, blank=True, null=True)
    out_date_and_time = models.DateField(null=True, blank=True)
    prepared_by_name = models.CharField(max_length=100, blank=True, null=True)
    prepared_by_email = models.CharField(max_length=100, blank=True, null=True)
    poc_at_venue_name = models.CharField(max_length=100, blank=True, null=True)
    approver_email = models.CharField(max_length=100, blank=True, null=True)
    truck_details = models.CharField(max_length=100, blank=True, null=True)
    contact_details = models.CharField(max_length=100, blank=True, null=True)
    driver_details = models.CharField(max_length=100, blank=True, null=True)
    purpose = models.CharField(max_length=100, blank=True, null=True)
    reason = models.CharField(max_length=100, blank=True, null=True)
    office_address = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    challan_number = models.CharField(max_length=100, blank=True, null=True)
    maker_email = models.CharField(max_length=100, blank=True, null=True)
    checker_email = models.CharField(max_length=100, blank=True, null=True)
    

    approve_order = models.BooleanField(default=False)
    order_dispatch = models.BooleanField(default=False)


class OrderAttachFile(models.Model):
    order_id = models.ForeignKey(OrderDetail, on_delete= models.CASCADE)
    attached_file = models.FileField(upload_to="media/", default=None, null=True, blank=True)


class OrderComment(models.Model):
    order_id = models.ForeignKey(OrderDetail, on_delete= models.CASCADE)
    comment = models.CharField(max_length=100, null=True, blank=True)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)






# class OrderTime(models.Model):
#      asset_id = models.ForeignKey(AssetMaster, on_delete=models.SET_NULL, null=True)
#      order_detail = models.ForeignKey(OrderDetail, on_delete=models.SET_NULL, null=True)
    


class OrderHistory(models.Model):

    order_id =models.ForeignKey(OrderDetail, on_delete=models.CASCADE)

    #Customer Details
    customer_id = models.IntegerField(null=True, blank=True)
    customer = models.CharField(max_length=100, blank=True, null=True)
    completed_orders = models.CharField(max_length=100, blank=True, null=True)
    deployed_order = models.CharField(max_length=100, blank=True, null=True)
    taxed = models.CharField(max_length=100, blank=True, null=True)
    email_address = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    customer_revenue = models.CharField(max_length=100, blank=True, null=True)
    commercial_address = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField(null=True, blank=True, default=None)
    secondary_email = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

