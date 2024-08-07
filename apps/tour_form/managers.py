from django.db import models


class ActiveManager(models.Manager):
    def active(self):
        return super().get_queryset().filter(is_active=True)
