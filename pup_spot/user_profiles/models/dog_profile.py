from django.db import models

from .base_profile import BaseProfile

class DogProfile(BaseProfile):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='dog_profiles')
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    # avatar = models.ImageField() - We have to integrate this later

    def __str__(self):
        return f'{self.display_name} the {self.breed}'
    
    class Meta:
        app_label = 'pup_spot_profiles'
        verbose_name = 'Dog Profile'