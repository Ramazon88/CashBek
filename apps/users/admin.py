from django.contrib import admin

from apps.main.models import BlackListProducts
from apps.users.form import CustomUniversalForm, CustomUserCreationForm, CustomUniversalFormForUser
from apps.users.models import *
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

admin.site.register(Vendor)
admin.site.register(BlackListProducts)


class UserInline(admin.StackedInline):
    model = User
    form = CustomUserCreationForm
    can_delete = False
    min_num = 1
    max_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            self.form = CustomUniversalForm
        return super().get_formset(request, obj=None, **kwargs)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    exclude = ('password1', 'password2')
    inlines = [UserInline]
    list_display = ["name", "get_phone", "get_active"]

    def save_model(self, request, obj, form, change):
        obj.seller.user_type = SELLER
        obj.seller.auth_status = DONE
        obj.seller.is_staff = True
        super().save_model(request, obj, form, change)

    @admin.display(ordering='seller__phone', description='Телефон')
    def get_phone(self, obj):
        return obj.seller.phone

    @admin.display(ordering='seller__is_active', description='Актив', boolean=True)
    def get_active(self, obj):
        return obj.seller.is_active


@admin.register(Manager)
class SellerAdmin(admin.ModelAdmin):
    exclude = ('password1', 'password2')
    inlines = [UserInline]
    list_display = ["name", "get_phone", "get_active"]

    def save_model(self, request, obj, form, change):
        obj.manager.user_type = MANAGER
        obj.manager.auth_status = DONE
        obj.manager.is_staff = True
        super().save_model(request, obj, form, change)

    @admin.display(ordering='manager__phone', description='Телефон')
    def get_phone(self, obj):
        return obj.manager.phone

    @admin.display(ordering='manager__is_active', description='Актив', boolean=True)
    def get_active(self, obj):
        return obj.manager.is_active


@admin.register(Vendor_account)
class SellerAdmin(admin.ModelAdmin):
    exclude = ('password1', 'password2')
    inlines = [UserInline]
    list_display = ["name", "get_phone", "get_active"]

    def save_model(self, request, obj, form, change):
        obj.vendors.user_type = VENDOR
        obj.vendors.auth_status = DONE
        obj.vendors.is_staff = True
        super().save_model(request, obj, form, change)

    @admin.display(ordering='vendors__phone', description='Телефон')
    def get_phone(self, obj):
        return obj.vendors.phone

    @admin.display(ordering='vendors__is_active', description='Актив', boolean=True)
    def get_active(self, obj):
        return obj.vendors.is_active


class SimpleUserInline(admin.StackedInline):
    model = User
    form = CustomUserCreationForm
    can_delete = False
    min_num = 1
    max_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            self.form = CustomUniversalFormForUser
        return super().get_formset(request, obj=None, **kwargs)


@admin.register(SimpleUsers)
class SellerAdmin(admin.ModelAdmin):
    exclude = ('password1', 'password2')
    inlines = [SimpleUserInline]
    list_display = ["full_name", "get_phone", "pinfl", "auth_status", "get_active"]

    @admin.display(ordering='simple_user__phone', description='Телефон')
    def get_phone(self, obj):
        return obj.simple_user.phone

    @admin.display(ordering='simple_user__is_active', description='Актив', boolean=True)
    def get_active(self, obj):
        return obj.simple_user.is_active

    @admin.display(ordering='simple_user__first_name', description='Имя')
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @admin.display(ordering='simple_user__auth_status', description='Статус авторизации')
    def auth_status(self, obj):
        return obj.simple_user.auth_status


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
