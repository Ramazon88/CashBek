from django.contrib import admin

from apps.main.models import *

admin.site.register(TempPriceProduct)
admin.site.register(TempPromo)
admin.site.register(Promo)

admin.site.register(QR_code)
admin.site.register(Fribase)
admin.site.register(Notifications)
admin.site.register(ReadNot)
admin.site.register(FAQ)
admin.site.register(Token_confirm)

@admin.register(Cashbek)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["product", "created_at"]
    list_display_links = ["product"]
    search_fields = ["product__imei1"]
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["model", "imei1", "is_active"]
    list_display_links = ["model"]
    search_fields = ["imei1"]
    list_filter = ["is_active"]
