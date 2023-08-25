from rest_framework import serializers

from apps.main.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        exclude = ["vendor", "datetime", "is_active"]


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        exclude = ["telegram_id"]


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ["type_of_activity", "price"]


class GetCheckSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    seller = SellerSerializer()
    vendor = VendorSerializer()

    class Meta:
        model = Cashbek
        fields = ["id", "created_at", "product", "seller", "vendor", "amount", "types"]


class GetProductSerializer(serializers.ModelSerializer):
    ven = VendorSerializer()

    class Meta:
        model = Products
        fields = ["id", "ven", "model", "imei1", "sku"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update({"amount": PriceProduct.objects.filter(promo__status=ACTIVE, product_id=data["id"]).first().price})
        data.update({"image": "https://w7.pngwing.com/pngs/378/624/png-transparent-iphone-14.png"})
        return data
