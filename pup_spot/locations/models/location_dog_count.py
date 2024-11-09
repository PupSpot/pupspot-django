from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LocationDogCountReport(models.Model):
    location = models.ForeignKey(
        'locations.Location', 
        on_delete=models.CASCADE,
        related_name='dog_count_reports'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='dog_count_reports'
    )
    count = models.PositiveIntegerField(
        help_text="Number of dogs observed at the location"
    )
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reported_at']