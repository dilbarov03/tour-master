from django.urls import path

from .views import TourTypeListAPIView, CountryListAPIView, TourFormListCreateAPIView, TourOfferGetAPIView

urlpatterns = [
    path("tour-types/", TourTypeListAPIView.as_view(), name="tour_types"),
    path("countries/", CountryListAPIView.as_view(), name="countries"),
    path("form/", TourFormListCreateAPIView.as_view(), name="tour_form"),
    path("form/<int:id>/offer/", TourOfferGetAPIView.as_view(), name="tour_offer"),
]