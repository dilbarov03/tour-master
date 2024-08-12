from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .models import Tour, TourCategory, UserBooking
from .serializers import TourCategorySerializer, TourListSerializer, TourDetailSerializer, UserBookingSerializer


class TourCategoryListAPIView(generics.ListAPIView):
    queryset = TourCategory.objects.filter(is_active=True)
    serializer_class = TourCategorySerializer


class TourListAPIView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', )


class TourDetailAPIView(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourDetailSerializer

    def get_queryset(self):
        return Tour.objects.prefetch_related('prices').all()


class UserBookingCreateAPIView(generics.CreateAPIView):
    queryset = UserBooking.objects.all()
    serializer_class = UserBookingSerializer
