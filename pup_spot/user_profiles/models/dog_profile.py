from django.db import models

from .base_profile import BaseProfile

class DogProfile(BaseProfile):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='dog_profiles')
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    height = models.FloatField(help_text="Height in centimeters")
    weight = models.FloatField(help_text="Weight in kilograms")
    activity_level = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])
    friendliness = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.display_name} the {self.breed}'
    
    class Meta:
        app_label = 'user_profiles'
        verbose_name = 'Dog Profile'