from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import User


@receiver(post_save, sender=User)
def add_supervisor_group(sender, instance, created, **kwargs):
    if created and instance.user_type == "supervisor":
        instance.is_staff = True
        group = Group.objects.get_or_create(name="Supervisors")[0]

        codenames = [
            ('change_userbooking',), ('view_userbooking',),
            ('change_userbookingprice',), ('view_userbookingprice',),

            ('change_tourform',), ('view_tourform',),
            ('change_touroffer',), ('view_touroffer',),
            ('change_tourpeople',), ('view_tourpeople',),
        ]

        for codename in codenames:
            permission = Permission.objects.get(codename=codename[0])
            group.permissions.add(permission)

        instance.groups.add(group)
        instance.save()
