from django.contrib import admin

from apps.users.models import *
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _


class BookInline(admin.StackedInline):
    model = User
    fieldsets = (
        (_('Main'), {'fields': ('phone', 'password')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    inlines = [BookInline]

    def save_model(self, request, obj, form, change):
        obj.simple_user.user_type = MANAGER
        super().save_model(request, obj, form, change)


@admin.register(User)
class UserAdmin(DjangoUserAdmin, admin.ModelAdmin):
    fieldsets = (
        (_('Main'), {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'user_type', 'auth_status', 'phone',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'phone', 'first_name', 'last_name', 'user_type',),
        }),
    )
    list_display = ('get_fullname', 'phone', 'is_staff', 'user_type', 'date_joined',)
    list_filter = ('user_type',)
    search_fields = ('first_name', 'last_name', 'phone',)
    ordering = ('-id',)

    @staticmethod
    def get_fullname(obj):
        if obj.first_name or obj.last_name:
            return "{} {}".format(obj.first_name, obj.last_name)
        return "{}".format(obj.username)
