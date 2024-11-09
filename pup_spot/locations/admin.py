from django.contrib import admin
from .models import Location, LocationRating, LocationDogCountReport, LocationCrowdMeter, LocationComment

admin.site.register(Location)
admin.site.register(LocationRating)
admin.site.register(LocationDogCountReport)
admin.site.register(LocationCrowdMeter)
admin.site.register(LocationComment)
