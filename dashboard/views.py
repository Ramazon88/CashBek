from django.shortcuts import render, redirect
from django.contrib.admin import site


def start(request):
    apps = site.get_app_list(request)
    print(apps)
    return render(request, "index.html")