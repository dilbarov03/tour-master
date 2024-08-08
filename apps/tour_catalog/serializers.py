from rest_framework import serializers

from .models import Tour, TourCategory, TourPrice


class TourCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourCategory
        fields = ('id', 'name')


class TourListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ('id', 'name', 'image', 'start_date', 'days_count', 'people_count', 'min_price')


class TourPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPrice
        fields = ('id', 'name', 'price', 'people_count')


class TourDetailSerializer(serializers.ModelSerializer):
    prices = TourPriceSerializer(many=True)

    class Meta:
        model = Tour
        fields = ('id', 'name', 'image', 'description', 'prices')
