from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LocationCrowdMeter(models.Model):
    """
    Tracks the overall crowdedness of a location on a scale of 1-10.
    
    This metric measures the general busyness of a location, including both people 
    and dogs. This is distinct from the dog count metric, which specifically tracks 
    the number of dogs present. The crowd meter helps users find locations that 
    match their comfort level with crowds, regardless of the specific dog population.
    
    Scale interpretation:
    1-3: Very quiet/empty
    4-6: Moderately busy
    7-8: Busy
    9-10: Very crowded
    """
    location = models.ForeignKey(
        'locations.Location', 
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