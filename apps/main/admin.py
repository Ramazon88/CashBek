from django.contrib import admin

from apps.main.models import *

# admin.site.register(TempPriceProduct)
# admin.site.register(TempPromo)
# admin.site.register(Promo)
#
# admin.site.register(QR_code)
# admin.site.register(Fribase)
admin.site.register(Notifications)
# admin.site.register(ReadNot)
admin.site.register(FAQ)


# Admin panel for super admin

class SuperAdmin(admin.AdminSite):
    site_header = "Super Cashbek"


superAdmin = SuperAdmin(name="SuperCashbek")
superAdmin.register(TempPriceProduct)
superAdmin.register(TempPromo)
superAdmin.register(Promo)
superAdmin.register(Token_confirm)

superAdmin.register(QR_code)
superAdmin.register(Fribase)
superAdmin.register(Notifications)
superAdmin.register(ReadNot)
superAdmin.register(FAQ)


class CashbekAdmin(admin.ModelAdmin):
    list_display = ["get_product_model", "get_product_imei", "get_user", "created_at"]
    list_display_links = ["get_product_model"]
    search_fields = ["product__imei1"]
    list_filter = ["created_at", "vendor"]


superAdmin.register(Cashbek, CashbekAdmin)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ["model", "imei1", "is_active"]
    list_display_links = ["model"]
    search_fields = ["imei1"]
    list_filter = ["is_active"]


superAdmin.register(Products, ProductsAdmin)
