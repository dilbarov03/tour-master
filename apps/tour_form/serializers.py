from rest_framework import serializers

from .models import TourType, Country, City, TourPeople, TourForm, TourOffer


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


class TourPeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPeople
        fields = ("id", "full_name", "birth_date", "gender")


class TourFormSerializer(serializers.ModelSerializer):
    tour_people = TourPeopleSerializer(many=True)
    has_answered = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = TourForm
        fields = ("id", "room_count", "tour_type", "country", "city",
                  "from_date", "to_date", "holidays", "phone", "comment", "tour_people",
                  "has_answered", "status", "full_name")

    def create(self, validated_data):
        tour_people_data = validated_data.pop("tour_people")
        user = self.context["request"].user
        tour_form = TourForm.objects.create(user=user, **validated_data)
        for tour_people_data in tour_people_data:
            TourPeople.objects.create(tour_form=tour_form, **tour_people_data)
        return tour_form

    def get_has_answered(self, obj):
        return obj.answered_at is not None

    def get_status(self, obj):
        return obj.tour_offer.status if hasattr(obj, "tour_offer") else "new"

    def get_full_name(self, obj):
        person = obj.tour_people.first()
        return person.full_name if person else ""


class TourOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourOffer
        fields = ("id", "image", "text", "status")
        read_only_fields = ("image", "text")

    def validate(self, attrs):
        if self.instance and self.instance.status != "new":
            raise serializers.ValidationError("You can't update this offer")
        return attrs
