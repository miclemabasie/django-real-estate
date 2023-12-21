from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from apps.ratings.serializers import RatingSerializer

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    full_name = serializers.SerializerMethodField(read_only=True)
    email = serializers.CharField(source="user.email")
    full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    country = serializers.CharField(source="country.name", read_only=True)
    reviews = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "full_name",
            "phone_number",
            "about_me",
            "license",
            "profile_photo",
            "gender",
            "country",
            "city",
            "is_buyer",
            "is_seller",
            "is_agent",
            "top_agent",
            "rating",
            "reviews",
            "num_reviews",
        ]

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    # def get_country(self, obj):
    #     return obj.country.name

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = RatingSerializer(reviews, many=True)
        return serializer.data

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        if instance.top_agent:
            ret["top_agent"] = True
        return ret


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "profile_photo",
            "about_me",
            "license",
            "gender",
            "country",
            "city",
            "is_buyer",
            "is_seller",
            "is_agent",
        ]

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        if instance.top_agent:
            ret["top_agent"] = True
        return ret
