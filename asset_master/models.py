from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
import datetime



class AssetMasterAccessories(models.Model):

    class RepairType(models.IntegerChoices):
            DEFAULT_TYPE = 10
            EXTERNAL_REPAIR = 20,
            INTERNAL_REPAIR = 30,
    
    class RelationshipType(models.IntegerChoices):
        PARENT = 101
        CHILD = 102
            
                
    area = models.CharField(max_length=100, null=True, blank=True)
    fc_no = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    sub_category = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    model_no = models.CharField(max_length=100, null=True, blank=True)
    serial_no = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    asset_tag = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    age = models.CharField(null=True, blank=True, max_length=100)
    box_number = models.CharField(max_length=100, null=True, blank=True, default="")
    last_service_date = models.DateField(null=True, blank=True, default=None)
    upcoming_service_date = models.DateField(null=True, blank=True, default=None)

    # unit of measurement
    length = models.CharField(max_length=100, null=True, blank=True)
    breadth = models.CharField(max_length=100, null=True, blank=True)
    height = models.CharField(max_length=100, null=True, blank=True)
    width = models.CharField(max_length=100, null=True, blank=True)

    #Product engineering support info
    warranty_period = models.CharField(max_length=100, null=True, blank=True)
    under_amc = models.BooleanField(default=False)
    amc_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)

    #Asset in and out tracking
    storage_warehouse_number = models.CharField(max_length=100, null=True, blank=True)
    availability = models.BooleanField(default=False)
    outward_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    outward_remarks = models.CharField(max_length=100, null=True, blank=True)
    inward_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    inward_remarks = models.CharField(max_length=100, null=True, blank=True)

    #Purchase
    vendor = models.CharField(max_length=100, null=True, blank=True)
    purchased_on = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    cost_price = models.CharField(max_length=100, null=True, blank=True)
    tax_rate = models.CharField(max_length=100, null=True, blank=True)
    depricated_value = models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)

    #Pricing
    rented_asset = models.BooleanField(default=False)
    rental_pricing = models.CharField(max_length=100, null=True, blank=True)
    rent_collected = models.CharField(max_length=100, null=True, blank=True)
    available_for_sale = models.CharField(max_length=100, null=True, blank=True)

    #Usage information
    asset_utilization = models.CharField(max_length=100, null=True, blank=True)

    #Asset status
    asset_status = models.CharField(max_length=100, null=True, blank=True, default="available")
    repair_type = models.IntegerField(choices=RepairType.choices, default=RepairType.DEFAULT_TYPE)

    #Sold assets
    sold_asset = models.BooleanField(default=False)

    #Loan status
    loaned_asset = models.BooleanField(default=False)
    loan_period = models.CharField(max_length=100, null=True, blank=True)

    #Add to order
    add_to_order = models.BooleanField(default=False)

    #Added to confirm order
    confirm_order = models.BooleanField(default=False)

    owner = models.CharField(max_length=100, null=True, blank=True, default='Zoom Communication')

    mapping = models.CharField(max_length=100, null=True, blank=True)

    relation = models.IntegerField(choices=RelationshipType.choices, default=RelationshipType.CHILD) 

    image = models.ImageField(upload_to="media/", default=None, null=True, blank=True)




#Asset master model
class AssetMaster(models.Model):

    class RepairType(models.IntegerChoices):
            DEFAULT_TYPE = 10
            EXTERNAL_REPAIR = 20,
            INTERNAL_REPAIR = 30,
    
    class RelationshipType(models.IntegerChoices):
        PARENT = 101
        CHILD = 102
            
                
    area = models.CharField(max_length=100, null=True, blank=True)
    fc_no = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    sub_category = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    model_no = models.CharField(max_length=100, null=True, blank=True)
    serial_no = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    asset_tag = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    age = models.CharField(null=True, blank=True, max_length=100)
    box_number = models.CharField(max_length=100, null=True, blank=True, default="")
    last_service_date = models.DateField(null=True, blank=True, default=None)
    upcoming_service_date = models.DateField(null=True, blank=True, default=None)

    # unit of measurement
    length = models.CharField(max_length=100, null=True, blank=True)
    breadth = models.CharField(max_length=100, null=True, blank=True)
    height = models.CharField(max_length=100, null=True, blank=True)
    width = models.CharField(max_length=100, null=True, blank=True)

    #Product engineering support info
    warranty_period = models.CharField(max_length=100, null=True, blank=True)
    under_amc = models.BooleanField(default=False)
    amc_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)

    #Asset in and out tracking
    storage_warehouse_number = models.CharField(max_length=100, null=True, blank=True)
    availability = models.BooleanField(default=False)
    outward_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    outward_remarks = models.CharField(max_length=100, null=True, blank=True)
    inward_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    inward_remarks = models.CharField(max_length=100, null=True, blank=True)

    #Purchase
    vendor = models.CharField(max_length=100, null=True, blank=True)
    purchased_on = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    cost_price = models.CharField(max_length=100, null=True, blank=True)
    tax_rate = models.CharField(max_length=100, null=True, blank=True)
    depricated_value = models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)

    #Pricing
    rented_asset = models.BooleanField(default=False)
    rental_pricing = models.CharField(max_length=100, null=True, blank=True)
    rent_collected = models.CharField(max_length=100, null=True, blank=True)
    available_for_sale = models.CharField(max_length=100, null=True, blank=True)

    #Usage information
    asset_utilization = models.CharField(max_length=100, null=True, blank=True)

    #Asset status
    asset_status = models.CharField(max_length=100, null=True, blank=True, default="available")
    repair_type = models.IntegerField(choices=RepairType.choices, default=RepairType.DEFAULT_TYPE)

    #Sold assets
    sold_asset = models.BooleanField(default=False)

    #Loan status
    loaned_asset = models.BooleanField(default=False)
    loan_period = models.CharField(max_length=100, null=True, blank=True)

    #Add to order
    add_to_order = models.BooleanField(default=False)

    #Added to confirm order
    confirm_order = models.BooleanField(default=False)

    owner = models.CharField(max_length=100, null=True, blank=True, default='Zoom Communication')

    mapping = models.CharField(max_length=100, null=True, blank=True)

    relation = models.IntegerField(choices=RelationshipType.choices, default=RelationshipType.PARENT) 

    # asset_accessories = models.ManyToManyField(AssetMasterAccessories, related_name='asset_accessory', blank=True)

    image = models.ImageField(upload_to="media/", default=None, null=True, blank=True)






#Asset Master comment...
class AssetMasterComment(models.Model):
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    asset_id = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Comment of { self.asset_id}"


#Asset Master attach comments...
class AssetMasterAttachFile(models.Model):
    asset_id = models.ForeignKey(AssetMaster, on_delete= models.CASCADE)
    attached_file = models.FileField(upload_to="media/", default=None, null=True, blank=True)



#Asset master inventory history...
class AssetMasterInventory(models.Model):
    class AssetTransfer(models.IntegerChoices):
            SEND_TRANSFER_REQUEST = 1,
            TRANSFER_REQUEST_SENT = 2,
            READY_TO_TRANSFER = 3,
            TRANSFERED = 4,
    asset_transfer = models.IntegerField(choices=AssetTransfer.choices, default=AssetTransfer.SEND_TRANSFER_REQUEST)   
    asset_id = models.ForeignKey(AssetMaster, on_delete=models.CASCADE)
    move_to_inventory = models.BooleanField(default=False)
    order_id = models.PositiveIntegerField(null=True, blank=True)




#Custom user...
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        user = self.model(
            email = self.normalize_email(email),**extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user( email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True, db_index=True, max_length=200)
    password = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']