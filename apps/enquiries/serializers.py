from rest_framework import serializers

from .models import Enquiry


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = "__all__"


class CreateEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = ("id", "name", "phone_number", "email", "subject", "message")
