from django.contrib import admin

from main.models import ShippingFee


@admin.register(ShippingFee)
class ShippingFeeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
    ]


# @admin.register(State)
# class StateAdmin(admin.ModelAdmin):
#     pass


# @admin.register(District)
# class DistrictAdmin(admin.ModelAdmin):
#     pass
