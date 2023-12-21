import random
import string

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class ProperyPublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published_status=True)


class Property(TimeStampedUUIDModel):
    """Model definition for Property."""

    class AvertTypeChoices(models.TextChoices):
        FOR_SALE = "For Sale", _("For Sale")
        FOR_RENT = "For Rent", _("For Rent")
        AUCTION = "Auction", _("Auction")

    class PropertyTypeChoices(models.TextChoices):
        HOUSE = "House", _("House")
        APARTMENT = "Apartment", _("Apartment")
        LAND = "Land", _("Land")
        COMMERCIAL = "Commercial", _("Commercial")
        INDUSTRIAL = "Industrial", _("Industrial")
        OFFICE = "Office", _("Office")
        STORAGE = "Storage", _("Storage")
        PARKING = "Parking", _("Parking")
        OTHER = "Other", _("Other")

    user = models.ForeignKey(
        User,
        related_name="agent_buyer",
        verbose_name=_("Agent, Seller or Buyer"),
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(verbose_name=_("Property Title"), max_length=255)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    ref_code = models.CharField(
        verbose_name=_("Reference Code"), max_length=255, null=True, blank=True
    )
    description = models.TextField(
        verbose_name=_("Property Description"),
        default="default description.. Update me please...",
    )
    country = CountryField(
        verbose_name=_("Country"), default="CM", blank_label="Select Country"
    )
    city = models.CharField(verbose_name=_("City"), max_length=255, default="Bamenda")
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=255, default="140-001"
    )
    street_address = models.CharField(verbose_name=_("Street Address"), max_length=255)

    property_number = models.IntegerField(
        verbose_name=_("Property Number"),
        validators=[MinValueValidator(1)],
        default=112,
    )
    price = models.DecimalField(
        verbose_name=_("Property Price"), max_digits=8, decimal_places=2, default=0.00
    )
    tax = models.DecimalField(
        verbose_name=_("Property Tax"),
        max_digits=6,
        decimal_places=2,
        default=0.00,
        help_text="15% property tax charged on the property price",
    )
    plot_area = models.DecimalField(
        verbose_name=_("Area (sq ft)"), max_digits=8, decimal_places=2, default=0.0
    )
    bedrooms = models.PositiveIntegerField(verbose_name=_("Bedrooms"), default=1)
    total_floors = models.PositiveIntegerField(
        verbose_name=_("Numbor of Floors"), default=0
    )
    bathrooms = models.PositiveIntegerField(verbose_name=_("Bathrooms"), default=0)
    advert_type = models.CharField(
        verbose_name=_("Avert Type"),
        max_length=50,
        choices=AvertTypeChoices.choices,
        default="For Sale",
    )
    property_type = models.CharField(
        verbose_name=_("Property Type"),
        max_length=20,
        choices=PropertyTypeChoices.choices,
        default="Other",
    )
    cover_photo = models.ImageField(
        verbose_name=_("Main Photo"),
        upload_to="photos",
        default="/house_sample.jpg",
        null=True,
        blank=True,
    )
    photo_1 = models.ImageField(
        verbose_name=_("Main Photo"),
        upload_to="photos",
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )

    photo_2 = models.ImageField(
        verbose_name=_("Main Photo"),
        upload_to="photos",
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )

    photo_3 = models.ImageField(
        verbose_name=_("Main Photo"),
        upload_to="photos",
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    published_status = models.BooleanField(verbose_name=_("Published"), default=False)
    views = models.PositiveIntegerField(verbose_name=_("Total Views"), default=0)

    currency = models.CharField(
        verbose_name=_("Currency"), max_length=3, default="USD", null=True, blank=True
    )
    garages = models.PositiveIntegerField(
        verbose_name=_("Garages"), default=0, null=True, blank=True
    )
    area_measurement = models.CharField(
        verbose_name=_("Area Measurement"),
        max_length=20,
        default="sq ft",
        null=True,
        blank=True,
    )
    year_built = models.PositiveIntegerField(
        verbose_name=_("Year Built"), default=0, null=True, blank=True
    )

    objects = models.Manager()
    published = ProperyPublishedManager()

    class Meta:
        """Meta definition for Property."""

        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        """Unicode representation of Property."""
        return self.title

    def get_absolute_url(self):
        """Return absolute url for Property."""
        return reverse(
            "properties:property_detail", args=[str(self.slug)]
        )  # TODO: Fix this

    def save(self, *args, **kwargs):
        """Save method for Property. modify the ref_code field using random string from string library"""
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "REF-"
        self.ref_code += "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Property, self).save(*args, **kwargs)

    @property
    def final_property_price(self):
        """Return the final price of the property after tax"""
        tax_percentage = self.tax
        property_price = self.price
        tax_amount = round(tax_percentage * property_price, 2)
        price_after_tax = float(round(property_price + tax_amount))
        return price_after_tax


class PropertyViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("IP Address"), max_length=255)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="property_views"
    )

    def __str__(self):
        return f"Total views on - {self.property.title} by {self.ip} is - {self.property.views} view(s)"

    class Meta:
        verbose_name = "Total Views on Property"
        verbose_name_plural = "Total Property Views"
        ordering = ["-created_at"]
