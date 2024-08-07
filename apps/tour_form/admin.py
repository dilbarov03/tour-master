from django.contrib import admin

from .models import TourType, Country, City, TourPeople, TourOffer, TourForm


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
class TourFormAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "region", "tour_type", "country", "from_date", "to_date", "phone"]
    list_filter = ["user", "region", "tour_type", "country"]
    list_per_page = 25
    inlines = [TourPeopleInline]


@admin.register(TourOffer)
class TourOfferAdmin(admin.ModelAdmin):
    list_display = ["tour_form", "status"]
    list_filter = ["tour_form"]
    list_per_page = 25
    ordering = ["-created_at"]
