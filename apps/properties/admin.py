from django.contrib import admin

from .models import Property, PropertyViews


class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "ref_code",
        "country",
        "city",
        "postal_code",
        "price",
        "property_type",
        "published_status",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "published_status",
        "created_at",
        "updated_at",
        "country",
        "city",
        "property_type",
    )
    search_fields = ("title", "description", "country", "city", "property_type")
    # prepopulated_fields = {"slug": ("title",)}


admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyViews)
