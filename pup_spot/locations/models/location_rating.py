from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LocationRating(models.Model):
    location = models.ForeignKey('locations.Location', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField(
        help_text="Rating value from 0 to 5",
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['location', 'user']