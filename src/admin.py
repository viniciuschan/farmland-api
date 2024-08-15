from django.contrib import admin

from src.models import Farm, Farmer, Location

admin.site.register(Farmer)
admin.site.register(Location)
admin.site.register(Farm)
