from django.db.models import Sum
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.api.permissions import UserPermission
from apps.api.qr.serializers import GetTokenSerializer, CashbekSerializer
from apps.api.qr.service import get_vendor_balance
from apps.main.models import *
from apps.main.task import edit_qr_done, delete_token, check_promo


class TokenView(GenericAPIView):
    permission_classes = (UserPermission,)

    def post(self, request):
        user = self.request.user.simple_user
        serializer = GetTokenSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        now = timezone.now()
        qr = QR_code.objects.get(qr_id=serializer.data.get("qr_id"), is_used=False, expiry_date__gt=now)
        product = qr.product
        vendor = qr.product.ven
        seller = qr.seller
        balance = get_vendor_balance(user=user.pk, vendor=vendor)
        cashbek = PriceProduct.objects.filter(promo__status=ACTIVE, product=product)
        token = Token_confirm.objects.create(product=product, user=user, vendor=vendor, seller=seller, types=qr.types)
        data = {
            "product": {
                "id": product.id,
                "model": product.model,
                "imei1": product.imei1,
                "sku": product.sku,
                "cashbek": cashbek.first().price if cashbek.exists() else 0,
            },
            "vendor": {
                "id": vendor.id,
                "name": vendor.name,
                "logo": self.request.build_absolute_uri(vendor.logo.url),
                "balance": balance,
            },
            "seller": {
                "name": seller.name,
                "seller_name": seller.seller_name,
            },
            "token": token.token,
            "types": token.types,
        }
        edit_qr_done.delay(qr.chat_id, qr.message_id, qr.pk)

        return Response({"success": True, "result": data}, status=200)


class CashbekView(GenericAPIView):
    permission_classes = (UserPermission,)

    def post(self, request):
        user = self.request.user.simple_user
        serializer = CashbekSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        now = timezone.now()
        token = Token_confirm.objects.get(token=serializer.data.get("token_id"), is_used=False, expiry_date__gt=now)
        if token.user != user:
            data = {
                'success': False,
                'code': '120',
                'message': "Token is incorrect or expired"
            }
            return Response(data, status=400)
        product = token.product
        vendor = token.vendor
        seller = token.seller
        balance = get_vendor_balance(user=user.pk, vendor=vendor)
        given_amount = serializer.data.get("amount", None)
        success = {
            "success": True,
            "types": token.types,
            "income": 0,
            "expense": 0
        }
        if token.types == 2:
            if given_amount is None:
                return Response({"success": False, "code": "101", "message": "The required lines are not filled"},
                                status=400)
            if given_amount > balance:
                return Response(
                    {"success": False, "code": "121", "message": "The given amount is more than the real balance"},
                    status=400)
            Cashbek.objects.create(amount=given_amount, price=given_amount, vendor=vendor, user=user, seller=seller,
                                   product=product, types=EXPENSE)
            success["expense"] = given_amount

        cashbek = PriceProduct.objects.filter(promo__status=ACTIVE, product=product)
        incom = Cashbek.objects.filter(active=True, types=1)
        promo = product.promo.filter(start__lte=now, end__gte=now, status=ACTIVE)
        print(promo)

        if token.types == 1 or promo.exists():
            incom_sum = incom.filter(promo=promo.first()).aggregate(Sum('price'))['price__sum'] if \
                incom.filter(promo=promo.first()).aggregate(Sum('price'))['price__sum'] else 0
            if promo.first().budget > incom_sum:
                budget = promo.first().budget - incom_sum
                if budget > cashbek.first().all_price:
                    amount = cashbek.first().all_price
                    description = ""
                else:
                    amount = budget
                    description = "Последний остаток был приравнен к бюджету"
                cashbek = Cashbek.objects.create(promo=promo.first(),
                                                 amount=round(amount * promo.first().price_procent / 100, ndigits=-3),
                                                 price=amount, vendor=vendor, user=user, seller=seller, product=product,
                                                 types=INCOME, description=description)
                success["income"] = int(cashbek.amount)
                check_promo.delay(promo.first().pk)
        product.is_active = False
        product.save()
        delete_token.delay(token.pk)

        return Response(success, status=200)
