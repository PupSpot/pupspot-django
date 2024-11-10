from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password

class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    
    # Required for Django's auth system
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        app_label = 'user_profiles'
        verbose_name = 'User Profile'

    @property
    def dog_profiles(self):
        return self.dog_profiles.all()

    def create_location_rating(self, location, value):
        """Create a new rating for a location"""
        from locations.models import LocationRating
        return LocationRating.objects.create(
            location=location,
            user=self,
            value=value
        )

    def create_location_crowd_meter(self, location, value):
        """Create a new crowd meter report"""
        from locations.models import LocationCrowdMeter
        return LocationCrowdMeter.objects.create(
            location=location,
            user=self,
            value=value
        )

    def create_dog_count_report(self, location, count):
        """Create a new dog count report"""
        from locations.models import LocationDogCountReport
        return LocationDogCountReport.objects.create(
            location=location,
            user=self,
            count=count
        )