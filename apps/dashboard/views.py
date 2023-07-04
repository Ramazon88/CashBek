import os
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from openpyxl.reader.excel import load_workbook

from apps.main.models import *
from config.settings import BASE_DIR


def dashboard_access(user):
    if user.is_authenticated and user.is_dashboard():
        return True
    return False


def signin(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        remember = request.POST.get("remember")
        user = authenticate(username=phone, password=password)
        if user and user.is_dashboard():
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
                request.session.modified = True
            return redirect("index")
        else:
            messages.error(request, "Invalit login or password")
    return render(request, "login.html")


@user_passes_test(dashboard_access, login_url="signin")
def index(request):
    context = {"home": True}
    return render(request, "index.html", context)


@user_passes_test(dashboard_access, login_url="signin")
def products(request):
    products = Products.objects.filter(vendor__vendor=request.user.vendor.vendor).order_by("-id")
    alls = products
    active = products.filter(is_active=True)
    no_active = products.filter(is_active=False)
    if request.GET.get('q'):
        word = request.GET.get('q')
        products = products.filter(Q(model__icontains=word) | Q(imei1__icontains=word) | Q(sku__icontains=word))
    pagination = Paginator(products, 50)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)
    context = {"products": True, "objs": page_obj, "all_products": products, "all": alls, "active": active,
               "no_active": no_active}
    return render(request, "products.html", context)


@user_passes_test(dashboard_access, login_url="signin")
def export_example(request):
    file_location = BASE_DIR / 'file/example_products.xlsx'
    with open(file_location, 'rb') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="example_products.xlsx"'
    return response


@user_passes_test(dashboard_access, login_url="signin")
def import_products(request):
    file = request.FILES['file']
    filename = file.name
    if filename.split(".")[1] != "xlsx":
        messages.error(request, "The file should be in .xlsx format")
    else:
        products = Products.objects.all()
        error_import = []
        creator = []
        imei = []
        wb = load_workbook(file)
        sheet = wb.active
        for row in sheet.iter_rows(min_row=2, max_col=3):
            data = {"model": "", "sku": "", "imei1": "", "reason": ""}
            if row[0].value is None or row[1].value is None or row[2].value is None:
                data["model"] = row[0].value
                data["imei1"] = row[1].value
                data["sku"] = row[2].value
                data["reason"] = "Обязательные строки не заполняются"
                error_import.append(data)
                continue
            elif products.filter(imei1=row[1].value):
                data["model"] = row[0].value
                data["imei1"] = row[1].value
                data["sku"] = row[2].value
                data["reason"] = "Этот продукт указан"
                error_import.append(data)
                continue
            elif row[1].value in imei:
                data["model"] = row[0].value
                data["imei1"] = row[1].value
                data["sku"] = row[2].value
                data["reason"] = "Этот продукт указан"
                error_import.append(data)
                continue
            creator.append(
                BlackListProducts(model=row[0].value, imei1=row[1].value, sku=row[2].value, vendor=request.user.vendor))
            imei.append(row[1].value)
        context = {"products": True, "error": error_import, "correct": creator}
        if creator:
            obj = BlackListProducts.objects.bulk_create(creator)
            context["interval"] = f"{obj[0].id}-{obj[-1].id}"
        return render(request, "confirm_products.html", context)

    return redirect("products")


@user_passes_test(dashboard_access, login_url="signin")
def export_products(request):
    products = Products.objects.filter(vendor=request.user.vendor).order_by("-id")
    file_location = BASE_DIR / 'file/products.xlsx'
    file_send = BASE_DIR / f'file/products_{timezone.now().strftime("%d-%m-%Y")}.xlsx'
    wb = load_workbook(file_location)
    sheet = wb.active
    for i_row, user_data in enumerate(products, start=2):
        sheet.cell(row=i_row, column=1, value=user_data.model)
        sheet.cell(row=i_row, column=2, value=user_data.datetime.strftime("%d-%m-%Y"))
        sheet.cell(row=i_row, column=3, value=user_data.imei1)
        sheet.cell(row=i_row, column=4, value=user_data.sku)
        sheet.cell(row=i_row, column=5, value="Актив" if user_data.is_active else "Не актив")
    wb.save(file_send)
    with open(file_send, 'rb') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="products_{timezone.now().strftime("%d-%m-%Y")}.xlsx"'
    os.remove(file_send)
    return response


@user_passes_test(dashboard_access, login_url="signin")
def confirm_products(request):
    if request.POST.get("new_prs"):
        prs = request.POST.get("new_prs")
        prs = prs.split("-")
        creator = []
        objs = BlackListProducts.objects.filter(pk__gte=prs[0], pk__lte=prs[1], vendor=request.user.vendor)
        for obj in objs:
            creator.append(Products(model=obj.model, imei1=obj.imei1, sku=obj.sku, vendor=request.user.vendor))
        Products.objects.bulk_create(creator)
        objs.delete()
        messages.success(request, "Товары успешно добавлены")
        return redirect("products")






