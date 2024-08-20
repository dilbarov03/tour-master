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


class TourOfferInline(admin.StackedInline):
    model = TourOffer
    extra = 0
    readonly_fields = ["answered_by", "status"]

    def save_new_object(self, request, form, inline_formset):
        for form in inline_formset.forms:
            if form.instance.pk is None:
                form.instance.answered_by = request.user
        return form.instance

    # def has_delete_permission(self, request, obj=None):
    #     return False


@admin.register(TourForm)
class TourFormAdmin(ImportExportModelAdmin, ExportActionMixin):
    list_display = ["id", "user", "region", "branch", "tour_type", "country", "from_date", "to_date", "full_name",
                    "phone", "has_offer", "is_bought"]
    list_filter = ["region", "branch", "user", "created_at", "is_bought"]
    search_fields = ["user__username", "user__full_name", "full_name", "phone", "barcode"]
    list_per_page = 25
    inlines = [TourPeopleInline, TourOfferInline]
    readonly_fields = ["answered_at", ]
    resource_class = TourFormResource

    def save_formset(self, request, form, formset, change):
        if formset.model == TourOffer and formset.forms:
            inline_form = formset.forms[0]
            obj = inline_form.save(commit=False)
            if not obj.pk:  # New object, not yet saved
                obj.answered_by = request.user
                obj.save()  # Save to the database

                # Send notification for the new TourOffer object
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"user_{obj.tour_form.user.id}",
                    {
                        "type": "notify",
                        "event": "New Tour Offer",
                        "message": f"A new tour offer has been created.",
                        "tour_form": obj.tour_form.id
                    }
                )

        # Save the formset
        formset.save()
