from django.contrib import admin

from .models import Tour, TourCategory, TourPrice, UserBooking, UserBookingPrice


class TourPriceInline(admin.TabularInline):
    model = TourPrice
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    inlines = [TourPriceInline]
    list_display = ('id', 'name', 'category', 'start_date', 'days_count', 'people_count', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('category', 'start_date', 'is_active')
    search_fields = ('name', )


@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'order')
    list_filter = ('is_active', )
    search_fields = ('name', )


class UserBookingPriceInline(admin.TabularInline):
    model = UserBookingPrice
    extra = 0


@admin.register(UserBooking)
class UserBookingAdmin(admin.ModelAdmin):
    inlines = [UserBookingPriceInline]
    list_display = ('id', 'tour', 'user', 'full_name', 'total_price')
    list_filter = ('tour', 'user')
    search_fields = ('tour', 'user')