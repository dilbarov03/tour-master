from django.db import models
from django.utils import timezone


class TourManager(models.Manager):
    def all(self):
        return super().get_queryset().filter(
            is_active=True, category__is_active=True, start_date__gte=timezone.now().date(),
            people_count__gt=0
        )


class TourPriceManager(models.Manager):
    def all(self):
        return super().get_queryset().filter(people_count__gt=0)
