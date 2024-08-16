from decimal import Decimal

from django.db.models import Min, F
from rest_framework import serializers

from .models import Tour, TourCategory, TourPrice, UserBookingPrice, UserBooking
from ..common.utils import send_booking_message


class TourCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourCategory
        fields = ('id', 'name')


class TourListSerializer(serializers.ModelSerializer):
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Tour
        fields = ('id', 'name', 'image', 'start_date', 'days_count', 'people_count', 'min_price')

    # def get_min_price(self, obj):
    #     min_price = obj.prices.all().aggregate(Min('price'))['price__min']



class TourPriceSerializer(serializers.ModelSerializer):
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = TourPrice
        fields = ('id', 'name', 'price', 'people_count', 'final_price')


class TourDetailSerializer(serializers.ModelSerializer):
    prices = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ('id', 'name', 'image', 'description', 'prices')

    def get_prices(self, obj):
        user = self.context['request'].user
        prices = obj.prices.filter(people_count__gt=0).annotate(
            final_price=F('price') * (1 + Decimal(user.branch.coefficient / 100) if user.branch else 1)
        )
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
            user_booking_price = UserBookingPrice.objects.create(
                user_booking=booking, total_price=(tour_price_data['tour_price'].price * tour_price_data['count']) *
                                                    (1 + Decimal(user.branch.coefficient / 100) if user.branch else 1),
                tour_price=tour_price_data['tour_price'], count=tour_price_data['count']
            )
            total_price += user_booking_price.total_price

        booking.region = user.region
        booking.total_price = total_price
        booking.save()

        send_booking_message(booking)

        return booking
