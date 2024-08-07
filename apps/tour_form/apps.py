from django.apps import AppConfig


class TourFormConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tour_form'

    class Meta:
        verbose_name = 'Тур форма'
        verbose_name_plural = 'Тур форма'
        