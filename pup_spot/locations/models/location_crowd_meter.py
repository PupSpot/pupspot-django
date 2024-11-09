from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from locations.models.location import Location
from django.contrib.auth import get_user_model

User = get_user_model()

class LocationCrowdMeter(models.Model):
    location = models.ForeignKey(
        'Location', 
        on_delete=models.CASCADE,
        related_name='crowd_meter_reports'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='crowd_meter_reports'
    )
    value = models.FloatField(
        help_text="Scale of 1-10",
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(10.0)
        ]
    )
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reported_at']

    def __str__(self):
        return f"Crowd meter report by {self.user.username} at {self.location}"