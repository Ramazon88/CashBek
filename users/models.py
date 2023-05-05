from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from simple_history.models import HistoricalRecords

from users.manager import UserManager


# from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
# from rest_framework.serializers import ModelSerializer
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class User(AbstractUser):
    _validate_phone = RegexValidator(
        regex=r"^(!?){0}([998]){3}([3-9]){1}([0-9]){1}([0-9]){7}$",
        message=_("Your phone number must start with 9 and not exceed 12 characters. For example: 998993451545"),
    )
    """
    To store users
    """
    USER = 'user'
    SELLER = 'seller'
    VENDOR = 'vendor'
    MANAGER = 'manager'

    USER_TYPES = (
        (USER, _("User"),),
        (VENDOR, _("Vendor"),),
        (MANAGER, _("Manager"),),
        (SELLER, _("Seller"),)
    )
    NEW, CODE_VERIFIED, HALF, DONE = (
        "new",
        "code_verified",
        "half_done",
        "done"
    )

    AUTH_STATUS = (
        (NEW, _("NEW")),
        (CODE_VERIFIED, _("Code verified")),
        (HALF, _("Done without MyID")),
        (DONE, _("Done"))
    )
    phone = models.CharField(
        _('phone'),
        max_length=150,
        unique=True,
        help_text=_('Required. Enter valid phone number.'),
        error_messages={
            'unique': _("A user with that phone already exists."),
        },
        validators=_validate_phone
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    user_type = models.CharField(max_length=60, choices=USER_TYPES)
    auth_status = models.CharField(max_length=60, choices=AUTH_STATUS)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    history = HistoricalRecords()
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['user_type']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self):
        return self.get_full_name() or self.get_username()

