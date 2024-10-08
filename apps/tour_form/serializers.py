from rest_framework import serializers

from .models import TourType, Country, City, TourPeople, TourForm, TourOffer
from apps.users.verification import check_verification_status
from ..common.utils import send_form_message


class TourTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourType
        fields = ("id", "name")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name")


class CountrySerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ("id", "name", "cities")

    def get_cities(self, obj):
        cities = obj.cities.filter(is_active=True)
        return CitySerializer(cities, many=True).data


class TourPeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPeople
        fields = ("id", "full_name", "birth_date", "gender")


class TypeCountryCitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class TourFormSerializer(serializers.ModelSerializer):
    tour_people = TourPeopleSerializer(many=True)
    has_answered = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    barcode = serializers.CharField(read_only=True, source="tour_offer.barcode")
    price = serializers.DecimalField(max_digits=10, decimal_places=0, read_only=True,
                                     source="tour_offer.calculated_price")

    class Meta:
        model = TourForm
        fields = ("id", "room_count", "tour_type", "country", "city",
                  "from_date", "to_date", "holidays", "phone", "comment", "tour_people",
                  "has_answered", "status", "full_name", "barcode", "price")
        read_only_fields = ("barcode", "has_answered", "status", "price")

    def validate(self, attrs):
        tour_people = attrs["tour_people"]
        phone = attrs["phone"]
        if len(tour_people) == 0:
            raise serializers.ValidationError("At least one person should be in the tour")
        elif len(tour_people) > 15:
            raise serializers.ValidationError("Maximum 15 people can be in the tour")
        verification_status, message = check_verification_status(phone)
        if not verification_status:
            raise serializers.ValidationError("Phone number must be verified first")

        return attrs

    def create(self, validated_data):
        tour_people_data = validated_data.pop("tour_people")
        user = self.context["request"].user
        tour_form = TourForm.objects.create(user=user, region=user.region, branch=user.branch, **validated_data)
        for tour_people_data in tour_people_data:
            TourPeople.objects.create(tour_form=tour_form, **tour_people_data)
        send_form_message(tour_form)
        return tour_form

    def get_has_answered(self, obj):
        return obj.answered_at is not None

    def get_status(self, obj):
        return obj.tour_offer.status if hasattr(obj, "tour_offer") else "new"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tour_type"] = TypeCountryCitySerializer(instance.tour_type).data
        data["country"] = TypeCountryCitySerializer(instance.country).data
        data["city"] = TypeCountryCitySerializer(instance.city).data
        return data


class TourOfferSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=0, source="calculated_price")
    client = serializers.SerializerMethodField()
    travelers = serializers.SerializerMethodField()

    class Meta:
        model = TourOffer
        fields = ("id", "image", "text", "status", "price", "client", "travelers")
        read_only_fields = ("image", "text", "price", "client", "travelers")

    def validate(self, attrs):
        if self.instance and self.instance.status != "offered":
            raise serializers.ValidationError("You can't update this offer")
        return attrs

    def get_client(self, obj):
        return {
            "full_name": obj.tour_form.full_name,
            "phone": obj.tour_form.phone
        }

    def get_travelers(self, obj):
        return TourPeopleSerializer(obj.tour_form.tour_people, many=True).data
