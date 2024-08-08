import django_filters.rest_framework as filters
from rest_framework import generics

from .models import Tour, TourCategory
from .serializers import TourCategorySerializer, TourListSerializer, TourDetailSerializer


class TourCategoryListAPIView(generics.ListAPIView):
    queryset = TourCategory.objects.filter(is_active=True)
    serializer_class = TourCategorySerializer


class TourListAPIView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category', )


class TourDetailAPIView(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourDetailSerializer
