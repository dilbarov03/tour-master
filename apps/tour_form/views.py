from rest_framework import generics
import django_filters.rest_framework as filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import TourType, Country, City, TourOffer
from .serializers import TourTypeSerializer, TourFormSerializer, TourOfferSerializer, CountrySerializer


class TourTypeListAPIView(generics.ListAPIView):
    queryset = TourType.objects.all()
    serializer_class = TourTypeSerializer


class CountryListAPIView(generics.ListAPIView):
    serializer_class = CountrySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("tour_type",)

    def get_queryset(self):
        return Country.objects.all().prefetch_related("cities")


class TourFormListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TourFormSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.tour_forms.all()


class TourOfferGetAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TourOfferSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        tour_form_id = self.kwargs["id"]
        tour_offer = get_object_or_404(TourOffer, tour_form_id=tour_form_id)
        return tour_offer
