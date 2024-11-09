from django.contrib import admin
from .models import UserProfile, DogProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(DogProfile)