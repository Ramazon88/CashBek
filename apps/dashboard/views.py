from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.admin import site
from openpyxl.reader.excel import load_workbook

from config.settings import BASE_DIR


def index(request):
    context = {"home": True}
    return render(request, "index.html", context)


def products(request):
    context = {"products": True}
    return render(request, "products.html", context)


def export_example(request):
    file_location = BASE_DIR / 'file/example_products.xlsx'
    with open(file_location, 'rb') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="example_products.xlsx"'
    return response


def import_products(request):
    file = request.FILES['file']
    filename = file.name
    if filename.split(".")[1] != "xlsx":
        messages.error(request, "The file should be in .xlsx format")
    else:
        wb = load_workbook(file)
        sheet = wb.active
        for row in sheet.iter_rows(min_row=2, max_col=5):
            print(row[0].value)
            print(row[1].value)
            print(row[2].value)
            print(row[3].value)
            print(type(row[4].value))
        messages.success(request, "Your request is being processed. Wait for a telegram response")
    return redirect("products")
