from rest_framework import generics
import django_filters.rest_framework as filters

from .models import TourType, Country, City
from .serializers import TourTypeSerializer


class TourTypeListAPIView(generics.ListAPIView):
    queryset = TourType.objects.all()
    serializer_class = TourTypeSerializer


class CountryListAPIView(generics.ListAPIView):
    serializer_class = TourTypeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("tour_type",)

    def get_queryset(self):
        return Country.objects.prefetch_related("cities").all()
