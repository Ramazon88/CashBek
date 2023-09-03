from django.urls import path, include

urlpatterns = [
    path('auth/', include("apps.api.auth.urls")),
    path('balance/', include("apps.api.balance.urls")),
    path('nf/', include("apps.api.nf.urls")),
    path('qr/', include("apps.api.qr.urls")),
]

