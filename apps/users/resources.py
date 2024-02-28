from django.utils.timezone import localtime
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateTimeWidget
from config import settings
from .models import SimpleUsers


class TzDateTimeWidget(DateTimeWidget):

    def render(self, value, obj=None):
        if settings.USE_TZ:
            value = localtime(value)
        return super(TzDateTimeWidget, self).render(value)


class Resource(resources.ModelResource):
    created_at = Field(attribute="created_at", column_name="created_at",
                        widget=TzDateTimeWidget(format="%d.%m.%Y %H:%M:%S"))
    category = Field(attribute="simple_user__phone", column_name="phone")

    class Meta:
        model = SimpleUsers
        exclude = ("id", "doc_type_id", "doc_expiry_date", "doc_issued_by_id", "doc_type_id_cbu", "citizenship_id",
                   "citizenship_id_cbu", "nationality_id", "nationality_id_cbu", "birth_country_id",
                   "birth_country_id_cbu", "photo", "region_id", "region_id_cbu", "district_id", "district_id_cbu")
