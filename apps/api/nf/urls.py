from django.urls import path
from apps.api.nf.views import *

urlpatterns = [
    path('setFirebase/', SetFirebaseView.as_view()),
    path('getNotifications/', GetNotificationsView.as_view()),
    path('getNotificationsById/<int:pk>', GetNotificationsByIdView.as_view()),
    path('getFaq/', GetFaqView.as_view()),
]

