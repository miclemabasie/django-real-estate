import random
import string
from tabnanny import verbose
from unicodedata import decimal

from autoslug import AutoSlugField
import black
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from apps.common.models import TimeStampedUUIDModel
from django.db import models


class PropertyPublishedManager(models.Manager):
    def queryset(self):
        properties = super(PropertyPublishedManager, self).queryset.filter(
            published_status=True
        )
        return properties


User = get_user_model()


class Property(TimeStampedUUIDModel):
    class AdvertType(models.TextChoices):
        FOR_SALE = "For Sale", _("For Sale")
        FOR_RENT = "For Rent", _("For Rent")
        AUCTION = "Auction", _("Auction")

    class PropertyType(models.TextChoices):
        HOUSE = "House", _("House")
        APARTMENT = "Apartment", _("Apartment")
        OFFICE = "Office", _("Office")
        WAREHOUSE = "Warehouse", _("Warehouse")
        COMMERCIAL = "Commercial", _("Commercial")
        OTHER = "Other", _("Other")

    user = models.ForeignKey(
        User,
        verbose_name=_("Agent, Seller or Buyer"),
        related_name="agent_buyer",
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(verbose_name=_("Property Ttile"), max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    ref_code = models.CharField(
        verbose_name=_("Property Refrence Code"), max_length=255, null=True, blank=True
    )
    description = models.TextField(
        verbose_name=_("Descrioption"),
        default="Default description... update me please....",
    )
    country = CountryField(
        verbose_name=_("Country"), default="KE", blank_label="(Select Country)"
    )
    city = models.CharField(verbose_name=_("City"), max_length=180, default="Beau")
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=100, default="140"
    )
    street_address = models.CharField(
        verbose_name=_("Street Address"), max_length=150, default="KG8 Avenue"
    )
    property_number = models.IntegerField(
        verbose_name=_("Property Number"),
        validators=[MinValueValidator(1)],
        default=122,
    )
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.0
    )
    tax = models.DecimalField(
        verbose_name=_("Property Tax"),
        max_digits=6,
        decimal_places=2,
        default=0.15,
        help_text="15% property tax charged",
    )
    property_type = models.CharField(
        verbose_name=_("Property Type"),
        choices=PropertyType.choices,
        default=PropertyType.HOUSE,
        max_length=100,
    )
    plot_area = models.DecimalField(
        verbose_name=_("Plot Area(m^2"), max_digits=8, decimal_places=2, default=0.0
    )
    total_floors = models.IntegerField(verbose_name=_("Number of Floors"), default=0)
    bedrooms = models.IntegerField(verbose_name=_("Bedrooms"), default=1)
    bathrooms = models.DecimalField(
        verbose_name=_("Bathrooms"), max_digits=4, decimal_places=2, default=1.0
    )
    advert_type = models.CharField(
        verbose_name=_("Advert Type"),
        max_length=50,
        choices=AdvertType.choices,
        default=AdvertType.FOR_SALE,
    )

    cover_photo = models.ImageField(
        verbose_name=_("Cover Photo"),
        default="/house_sample.jpg",
        null=True,
        blank=True,
    )
    photo1 = models.ImageField(
        verbose_name=_("Photo1"),
        default="/inerior_sample.jpg",
        null=True,
        blank=True,
    )
    photo2 = models.ImageField(
        verbose_name=_("Photo2"),
        default="/inerior_sample.jpg",
        null=True,
        blank=True,
    )
    photo3 = models.ImageField(
        verbose_name=_("Photo3"),
        default="/inerior_sample.jpg",
        null=True,
        blank=True,
    )
    photo4 = models.ImageField(
        verbose_name=_("Photo4"),
        default="/inerior_sample.jpg",
        null=True,
        blank=True,
    )
    published_status = models.BooleanField(
        verbose_name=_("Pusblied Status"), default=False
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)

    objects = models.Manager()
    pupblished = PropertyPublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )

        super(Property, self).save(*args, **kwargs)

    @property
    def final_property_price(self):
        tax_percentage = self.tax
        property_price = self.price
        tax_amount = round(tax_percentage * property_price, 2)
        price_after_tax = float(round(property_price + tax_amount, 2))

        return price_after_tax


class PropertyViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("IP Address"), max_length=250)
    property = models.ForeignKey(
        Property, related_name="property_view", on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"Total view on -{self.property.title} is - {self.property.views} view(s)."
        )

    class Meta:
        verbose_name = "Total Views on Property"
        verbose_name_plural = "Total Property Views"
