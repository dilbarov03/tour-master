from django.urls import path

from .views import TourTypeListAPIView, CountryListAPIView

urlpatterns = [
    path("tour-types/", TourTypeListAPIView.as_view(), name="tour_types"),
    path("countries/", CountryListAPIView.as_view(), name="countries"),
]