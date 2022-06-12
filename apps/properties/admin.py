from django.contrib import admin
from .models import Property, ProPertyVeiws



class PropertyAdmin(admin.ModelAdmin):
    list_display = ["title", "country", "advert_type", "property_type"]

    list_filter = ["advert_type", "property_type", "country"]

admin.site.register(Property, PropertyAdmin)
admin.site.register(ProPertyVeiws)