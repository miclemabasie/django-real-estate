import logging

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import PropertyNotFound
from .models import Property, PropertyViews
from .pagination import PropertyPagination
from .serializers import (PropertyCreateSerializer, PropertySerializer,
                          PropertyViewSerializer)

logger = logging.getLogger(__name__)


class PropertyFilter(django_filters.FilterSet):
    advert_type = django_filters.CharFilter(
        field_name="advert_type", lookup_expr="iexact"
    )
    property_type = django_filters.CharFilter(
        field_name="property_type", lookup_expr="iexact"
    )
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Property
        fields = [
            "advert_type",
            "property_type",
            "price",
        ]

    # class Meta:
    #     model = Property
    #     fields = {
    #         "title": ["icontains"],
    #         "description": ["icontains"],
    #         "price": ["lte", "gte"],
    #         "bedrooms": ["lte", "gte"],
    #         "bathrooms": ["lte", "gte"],
    #         "garages": ["lte", "gte"],
    #         "for_sale": ["exact"],
    #         "for_rent": ["exact"],
    #         "city": ["exact"],
    #         "state": ["exact"],
    #         "country": ["exact"],
    #         "zip_code": ["exact"],
    #         "address": ["icontains"],
    #     }


class ListAllPropertyAPIView(generics.ListAPIView):
    """
    List all properties for a specific user or agent
    """

    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PropertyPagination
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = PropertyFilter
    search_fields = [
        "country",
        "city",
    ]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Property.objects.all()
        return Property.objects.filter(user=user).order_by("-created_at")


class ListAgentsPropertiesAPIView(generics.ListAPIView):
    """
    List all properties for a specific user or agent
    """

    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PropertyPagination
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = PropertyFilter
    search_fields = [
        "country",
        "city",
    ]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        # if user.is_staff:
        #     return Property.objects.all()
        return Property.objects.filter(user=user).order_by("-created_at")


class PropertyViewsAPIView(generics.ListAPIView):
    """List all property views"""

    serializer_class = PropertyViewSerializer
    queryset = PropertyViews.objects.all()


class PropertyDetailView(APIView):
    """
    Retrieve, update or delete a property instance.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, slug):
        try:
            return Property.objects.get(slug=slug)
        except Property.DoesNotExist:
            raise PropertyNotFound

    def get(self, request, slug, format=None):
        property = self.get_object(slug)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0]
        else:
            ip_address = request.META.get("REMOTE_ADDR")
        if not PropertyViews.objects.filter(
            property=property, ip_address=ip_address
        ).exists():
            PropertyViews.objects.create(property=property, ip_address=ip_address)
            property.views += 1
            property.save()
        serializer = PropertySerializer(property, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        property = self.get_object(pk)
        serializer = PropertyCreateSerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_property_api_view(request, slug):
    try:
        property = Property.objects.get(slug=slug)
    except Property.DoesNotExist:
        raise PropertyNotFound
    user = request.user
    if property.user != user:
        return Response(
            {
                "message": "You are not allowed to perform this action, property deos not belong to you"
            },
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "PUT":
        serializer = PropertyCreateSerializer(property, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_property_api_view(request):
    user = request.user
    data = request.data
    data["user"] = request.user.pkid
    if request.method == "POST":
        serializer = PropertyCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            logger.info(
                f"Property {serializer.data.get('title')} created by {user.email}"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_property_api_view(request, slug):
    try:
        property = Property.objects.get(slug=slug)
    except Property.DoesNotExist:
        raise PropertyNotFound
    user = request.user
    if property.user != user:
        return Response(
            {
                "message": "You are not allowed to perform this action, property deos not belong to you"
            },
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "DELETE":
        operation = property.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


@api_view(["POST"])
def uploadPropertyImage(request):
    if request.method == "POST":
        data = request.data
        property_id = data.get("property_id")
        property = Property.objects.get(id=property_id)
        property.cover_photo = request.FILES["cover_photo"]
        property.photo1 = request.FILES["photo1"]
        property.photo2 = request.FILES["photo2"]
        property.photo3 = request.FILES["photo3"]
        property.save()
        return Response("Image(s) uploaded", status=status.HTTP_200_OK)
    return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class PropertySearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PropertySerializer

    def post(self, request):
        queryset = Property.objects.filter(published_status=True)
        data = request.data

        advert_type = data["advert_type"]
        queryset = queryset.filter(advert_type__iexact=advert_type)
        property_type = data["property_type"]
        queryset = queryset.filter(property_type__iexact=property_type)
        price = data["price"]
        if price == "$0+":
            price = 0
        elif price == "$100,000+":
            price = 100000
        elif price == "$200,000+":
            price = 200000
        elif price == "$300,000+":
            price = 300000
        elif price == "$400,000+":
            price = 400000
        elif price == "$500,000+":
            price = 500000
        elif price == "$600,000+":
            price = 600000
        elif price == "Any":
            price = -1

        if price != -1:
            queryset = queryset.filter(price__gte=price)

        bedrooms = data["bedrooms"]
        if bedrooms == "0+":
            bedrooms = 0
        elif bedrooms == "1+":
            bedrooms = 1
        elif bedrooms == "2+":
            bedrooms = 2
        elif bedrooms == "3+":
            bedrooms = 3
        elif bedrooms == "4+":
            bedrooms = 4
        elif bedrooms == "5+":
            bedrooms = 5
        elif bedrooms == "6+":
            bedrooms = 6

        queryset = queryset.filter(bedrooms__gte=bedrooms)

        bathrooms = data["bathrooms"]
        if bathrooms == "0+":
            bathrooms = 0
        elif bathrooms == "1+":
            bathrooms = 1
        elif bathrooms == "2+":
            bathrooms = 2
        elif bathrooms == "3+":
            bathrooms = 3
        elif bedrooms == "4+":
            bedrooms = 4

        queryset = queryset.filter(bathrooms__gte=bathrooms)

        catch_phrase = data["catch_phrase"]
        queryset = queryset.filter(description__icontains=catch_phrase)

        serializer = PropertySerializer(queryset, many=True)

        return Response(serializer.data)
