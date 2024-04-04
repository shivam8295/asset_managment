from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "order_status", "order_dispatch", "organization")


@admin.register(OrderAttachFile)
class OrderDetailAttachFileAdmin(admin.ModelAdmin):
    list_display = ("id", "attached_file")


@admin.register(OrderComment)
class OrderDetailCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment")


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "customer"]


@admin.register(CustomerDetail)
class CustomerDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "completed_orders", "email_address", "customer_revenue", "email_address")


@admin.register(CustomerAttachFile)
class CustomerAttachFileAdmin(admin.ModelAdmin):
    list_display = ( "id","attached_file")


@admin.register(CustomerComment)
class CustomerCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "date_time")
