from django.shortcuts import render, redirect
from django.contrib.admin import site


def index(request):
    context = {"home": True}
    return render(request, "index.html", context)


def products(request):
    context = {"products": True}
    return render(request, "products.html", context)
