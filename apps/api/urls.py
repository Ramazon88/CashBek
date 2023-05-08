from django.urls import path, include

from apps.api.views import CreateUserView

urlpatterns = [
    path('sign/', CreateUserView.as_view())
]