from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class CustomUniversalForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("phone", "is_active")


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("phone",)


class CustomUniversalFormForUser(forms.ModelForm):

    class Meta:
        model = User
        fields = ("phone", "auth_status", "is_active", "date_joined", "last_login")
