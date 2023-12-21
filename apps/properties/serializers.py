from django_countries import countries
from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from .models import Property, PropertyViews


class PropertySerializer(CountryFieldMixin, serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    country = CountryField(country_dict=True)
    slug = serializers.SlugField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    final_property_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Property
        fields = (
            "id",
            "title",
            "user",
            "slug",
            "ref_code",
            "country",
            "city",
            "postal_code",
            "price",
            "tax",
            "final_property_price",
            "property_type",
            "published_status",
            "description",
            "created_at",
            "updated_at",
            "cover_photo",
            "photo_1",
            "photo_2",
            "photo_3",
            "plot_area",
            "total_floors",
            "bedrooms",
            "bathrooms",
            "garages",
            "street_address",
            "published_status",
            "views",
            "currency",
            "advert_type",
            "property_number",
            "area_measurement",
            "year_built",
        )

    def get_user(self, obj):
        return obj.user.username

    def get_final_property_price(self, obj):
        return obj.final_property_price


class PropertyCreateSerializer(serializers.ModelSerializer):
    country = CountryField(country_dict=True)

    class Meta:
        model = Property
        exclude = (
            "pkid",
            "slug",
            "created_at",
            "updated_at",
            "views",
            "published_status",
        )

    def get_user(self, obj):
        return obj.user.username


class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyViews
        exclude = ("updated_at", "pkid")
