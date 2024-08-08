from django.contrib import admin

from .models import Tour, TourCategory, TourPrice


class TourPriceInline(admin.TabularInline):
    model = TourPrice
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    inlines = [TourPriceInline]
    list_display = ('name', 'category', 'start_date', 'days_count', 'people_count', 'is_active')
    list_filter = ('category', 'start_date', 'is_active')
    search_fields = ('name', )


@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_filter = ('is_active', )
    search_fields = ('name', )
