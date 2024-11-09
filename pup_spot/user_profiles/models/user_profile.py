from django.db import models
from .base_profile import BaseProfile
from locations.models import LocationRating, LocationCrowdMeter, LocationDogCountReport
from django.contrib.auth.hashers import make_password, check_password

class UserProfile(BaseProfile):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Make sure to hash passwords before saving
    location = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username


    def check_password(self, raw_password):
        # Check password by comparing it with the hashed password
        return check_password(raw_password, self.password)

    class Meta:
        app_label = 'user_profiles'
        verbose_name = 'User Profile'

    @property
    def dog_profiles(self):
        return self.dog_profiles.all()

    def create_location_rating(self, location, value):
        """
        Create a new rating for a location
        Args:
            location: The Location instance to rate
            rating_value: Integer value of the rating (typically 1-5)
            comment: Optional comment string
        Returns:
            The created LocationRating instance
        """
        return LocationRating.objects.create(
            location=location,
            user=self,
            value=value
        )

    def create_location_crowd_meter(self, location, value):
        return LocationCrowdMeter.objects.create(
            location=location,
            user=self,
            value=value
        )

    def create_dog_count(self, location, count):
        return LocationDogCountReport.objects.create(
            location=location,
            user=self,
            count=count
        )