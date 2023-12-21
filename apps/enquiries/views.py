from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from real_estate.settings.development import DEFAULT_FROM_EMAIL

from .models import Enquiry


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def send_enquiry_email(request):
    data = request.data
    try:
        subject = data["subject"]
        name = data["name"]
        email = data["email"]
        message = data["message"]
        from_email = data["email"]
        recipient_list = [DEFAULT_FROM_EMAIL]
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        print(data["phone_number"])
        enquiry = Enquiry.objects.create(
            name=name,
            phone_number=data["phone_number"],
            email=email,
            subject=subject,
            message=message,
        )
        enquiry.save()
        return Response({"success": "Your enquiry has been sent"})
    except Exception as e:
        print(e)
        return Response({"error": "Something went wrong, please try again later"})
