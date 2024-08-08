from django.urls import path

from apps.tour_catalog.views import TourCategoryListAPIView, TourListAPIView, TourDetailAPIView, \
    UserBookingCreateAPIView

urlpatterns = [
    path("categories/", TourCategoryListAPIView.as_view(), name="tour_categories"),
    path("tours/", TourListAPIView.as_view(), name="tour_list"),
    path("tours/<int:pk>/", TourDetailAPIView.as_view(), name="tour_detail"),
    path("booking/", UserBookingCreateAPIView.as_view(), name="user_booking"),
]
