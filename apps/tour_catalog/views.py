from decimal import Decimal

from django.db.models import Min
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from .models import Tour, TourCategory, UserBooking
from .serializers import TourCategorySerializer, TourListSerializer, TourDetailSerializer, UserBookingSerializer


class TourCategoryListAPIView(generics.ListAPIView):
    queryset = TourCategory.objects.filter(is_active=True)
    serializer_class = TourCategorySerializer
    permission_classes = (IsAuthenticated,)


class TourListAPIView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category',)
    permission_classes = (IsAuthenticated,)


class TourListNewAPIView(generics.ListAPIView):
    serializer_class = TourListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('category',)
    pagination_class = None
    ordering = ('start_date',)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Tour.objects.filter(is_active=True).filter(
            is_active=True, category__is_active=True, start_date__gte=timezone.now().date(),
            people_count__gt=0).annotate(
            min_price=Min('prices__price') * (1 + Decimal(self.request.user.branch.coefficient) / 100)
            if self.request.user.branch else Min('prices__price')
        )


class TourDetailAPIView(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Tour.objects.prefetch_related('prices').all()


class UserBookingCreateAPIView(generics.CreateAPIView):
    queryset = UserBooking.objects.all()
    serializer_class = UserBookingSerializer
