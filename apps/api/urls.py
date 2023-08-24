from django.urls import path, include

urlpatterns = [
    path('auth/', include("apps.api.auth.urls")),
    path('balance/', include("apps.api.balance.urls")),
]

