from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AbiturientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'abiturient'

    verbose_name = _("Абитуриент")
