from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

from .models import Tour, TourCategory, TourPrice, UserBooking, UserBookingPrice
from .resources import UserBookingResource


class TourPriceInline(admin.TabularInline):
    model = TourPrice
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    inlines = [TourPriceInline]
    list_display = ('id', 'name', 'category', 'start_date', 'days_count', 'people_count', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('category', 'start_date', 'is_active')
    search_fields = ('name',)


@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name',)


class UserBookingPriceInline(admin.TabularInline):
    model = UserBookingPrice
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(UserBooking)
class UserBookingAdmin(ImportExportModelAdmin, ExportActionMixin):
    inlines = [UserBookingPriceInline]
    list_display = ('id', 'tour', 'user', 'region', 'branch', 'full_name', 'people_count', 'original_price_formatted',
                    'total_price_formatted', 'is_bought')
    list_filter = ("region", "branch", "user", "created_at", "is_bought")
    search_fields = ('user__full_name', 'tour__name', 'user__phone', 'tg_username', 'full_name')
    resource_class = UserBookingResource

    def get_queryset(self, request):
        if request.user.user_type == 'supervisor':
            return self.model.objects.filter(region=request.user.region)
        return super().get_queryset(request)

    def get_list_filter(self, request):
        if request.user.user_type == 'supervisor':
            return "branch", "created_at", "is_bought"
        return self.list_filter
