from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportActionMixin, ExportMixin

from .models import TourType, Country, City, TourPeople, TourOffer, TourForm
from .resources import TourFormResource


class CountryInline(admin.TabularInline):
    model = Country
    extra = 0


@admin.register(TourType)
class TourTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "order"]
    list_filter = ["is_active"]
    search_fields = ["name"]
    ordering = ["order"]
    inlines = [CountryInline]


class CityInline(admin.TabularInline):
    model = City
    extra = 0


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "tour_type", "is_active", "order"]
    list_filter = ["is_active", "tour_type"]
    search_fields = ["name"]
    ordering = ["order", "name"]
    inlines = [CityInline]


class TourPeopleInline(admin.TabularInline):
    model = TourPeople
    extra = 0


@admin.register(TourForm)
class TourFormAdmin(ImportExportModelAdmin, ExportActionMixin):
    list_display = ["id", "user", "region", "tour_type", "country", "from_date", "to_date", "phone"]
    list_filter = ["user", "region", "tour_type", "country"]
    list_per_page = 25
    inlines = [TourPeopleInline]
    readonly_fields = ["answered_at"]

    resource_class = TourFormResource


@admin.register(TourOffer)
class TourOfferAdmin(admin.ModelAdmin):
    list_display = ["tour_form", "answered_by", "status"]
    list_filter = ["tour_form"]
    list_per_page = 25
    ordering = ["-created_at"]
    readonly_fields = ["answered_by", "status"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.answered_by = request.user

            # Send a notification to the user
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{obj.tour_form.user.id}",  # Group name, based on user's ID
                {
                    "type": "notify",  # Method name that will be handled in the consumer
                    "event": "New Tour Offer",
                    "message": f"A new tour offer has been created by {request.user.id}"
                }
            )

        super().save_model(request, obj, form, change)

    # def has_delete_permission(self, request, obj=None):
    #     return False
