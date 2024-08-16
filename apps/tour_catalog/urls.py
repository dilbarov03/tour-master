from django.urls import path

from apps.tour_catalog.views import TourCategoryListAPIView, TourListAPIView, TourDetailAPIView, \
    UserBookingCreateAPIView, TourListNewAPIView

urlpatterns = [
    path("categories/", TourCategoryListAPIView.as_view(), name="tour_categories"),
    path("tours/", TourListAPIView.as_view(), name="tour_list"),
    path("tours/new/", TourListNewAPIView.as_view(), name="tour_list_new"),
    path("tours/<int:pk>/", TourDetailAPIView.as_view(), name="tour_detail"),
    path("booking/", UserBookingCreateAPIView.as_view(), name="user_booking"),
]
