from rest_framework import serializers

from .models import TourType, Country, City


class TourTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourType
        fields = ("id", "name")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name")


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True)

    class Meta:
        model = Country
        fields = ("id", "name", "cities")