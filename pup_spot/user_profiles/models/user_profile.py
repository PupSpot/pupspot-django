from django.db import models

from .base_profile import BaseProfile

class UserProfile(BaseProfile):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    bio = models.TextField()
    location = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.display_name

    class Meta:
        app_label = 'user_profiles'
        verbose_name = 'User Profile'
        

    @property
    def dog_profiles(self):
        return self.dog_profiles.all()