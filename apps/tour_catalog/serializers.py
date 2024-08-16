from rest_framework import serializers

from .models import Tour, TourCategory, TourPrice, UserBookingPrice, UserBooking
from ..common.utils import send_booking_message


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
    prices = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ('id', 'name', 'image', 'description', 'prices')

    def get_prices(self, obj):
        prices = obj.prices.filter(people_count__gt=0)
        serializer = TourPriceSerializer(prices, many=True)
        return serializer.data


class UserBookingPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookingPrice
        fields = ('id', 'count', 'tour_price')

    def validate(self, attrs):
        count = attrs.get('count')
        tour_price = attrs.get('tour_price')
        if count > tour_price.people_count:
            raise serializers.ValidationError('Количество человек больше, чем доступно')
        return attrs


class UserBookingSerializer(serializers.ModelSerializer):
    tour_prices = UserBookingPriceSerializer(many=True)

    class Meta:
        model = UserBooking
        fields = ('id', 'tour', 'full_name', 'phone', 'tg_username', 'tour_prices')

    def create(self, validated_data):
        tour_prices_data = validated_data.pop('tour_prices')
        user = self.context['request'].user
        booking = UserBooking.objects.create(user=user, **validated_data)

        total_price = 0
        for tour_price_data in tour_prices_data:
            user_booking_price = UserBookingPrice.objects.create(user_booking=booking, **tour_price_data)
            total_price += user_booking_price.total_price

        booking.region = user.region
        booking.total_price = total_price
        booking.save()

        send_booking_message(booking)

        return booking
