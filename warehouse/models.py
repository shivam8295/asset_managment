# from django.db import models
# from asset_master.models import AssetMaster


# class AvailableStatus(models.IntegerChoices):
#     AVAILABLE = 1
#     NOT_AVAILABLE = 0

# class Warehouse(models.Model):
#     serial_no = models.ForeignKey(AssetMaster, on_delete=models.CASCADE,null=False, blank=False)
#     available = models.IntegerField(choices=AvailableStatus.choices, null=True, blank=True)
#     outward_date = models.CharField(max_length=50, null=True, blank=True)
#     inward_date = models.CharField(max_length=50, null=True, blank=True)
#     inward = models.BooleanField(null=True, blank=True)
#     outward = models.BooleanField(null=True, blank=True)
#     in_field = models.BooleanField(null=True, blank=True)
#     out_field = models.BooleanField(null=True, blank=True)
#     remarks = models.CharField(max_length=100, null=True, blank=True)
#     warehouse = models.BooleanField(null=True, blank=True)

    # def __str__(self):
    #     return (self.inward_date)