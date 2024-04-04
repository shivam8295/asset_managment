from django.contrib import admin
from .models import *
@admin.register(AssetMaster)
class AssetMasterAdmin(admin.ModelAdmin):
    list_display = ("id", "asset_tag", "brand","fc_no", "serial_no","mapping", "relation", "image")



admin.site.register(CustomUser)
@admin.register(AssetMasterComment)
class AssetMastercommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "asset_id", "date_time")


@admin.register(AssetMasterAttachFile)
class AssetMasterAttachFile(admin.ModelAdmin):
    list_display = ("id", "attached_file", "asset_id" )


@admin.register(AssetMasterInventory)
class AssetMasterInventory(admin.ModelAdmin):
    list_display = ("id", "asset_id", "move_to_inventory", "order_id", "asset_transfer" )