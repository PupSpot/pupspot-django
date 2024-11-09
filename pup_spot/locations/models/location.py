from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Location(models.Model):
    # Basic location information
    
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)

    # Geolocation fields
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # User engagement fields
    likes = models.ManyToManyField(User, related_name='liked_locations', blank=True)
    ratings = models.IntegerField(default=0)
    crowd_meter = models.FloatField(
        blank=True, 
        null=True, 
        help_text="Scale of 1-10"
    )
    average_dog_count = models.IntegerField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        """Calculate average rating from all ratings"""
        if self.ratings == 0:
            return 0
        return self.ratings / self.total_ratings if hasattr(self, 'total_ratings') else 0

    @property
    def crowd_meter_value(self):
        """Return the crowd meter value, or 0 if not set"""
        return self.crowd_meter or 0

    @property
    def total_likes(self):
        """Count total number of likes"""
        return self.likes.count()

    @property
    def top_comment(self):
        """Return the most upvoted comment, or None if no comments exist"""
        return self.comments.annotate(
            vote_count=models.Count('votes')
        ).order_by('-vote_count', '-created_at').first()