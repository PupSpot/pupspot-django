from django.db import models
from django.contrib.auth import get_user_model
from locations.models.location_dog_count import LocationDogCountReport
from locations.models.location_crowd_meter import LocationCrowdMeter
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Location(models.Model):
    # Basic location information
    
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)

    # Geolocation fields
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # User engagement fields
    average_crowd_meter = models.FloatField(
        blank=True, 
        null=True, 
        help_text="Average crowdedness on scale of 1-10"
    )
    average_dog_count = models.IntegerField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.longitude}, {self.latitude}"

    ##
    # Properties

    @property
    def average_rating(self):
        """Calculate average rating from all ratings"""
        ratings = self.ratings.all()
        if not ratings.exists():
            return 0
        return sum(rating.value for rating in ratings) / ratings.count()

    @property
    def crowd_meter_value(self):
        """Return the crowd meter value, or 0 if not set"""
        return self.average_crowd_meter or 0

    @property
    def top_comment(self):
        """Return the most upvoted comment, or None if no comments exist"""
        return self.comments.annotate(
            vote_count=models.Count('votes')
        ).order_by('-vote_count', '-created_at').first()

    ##
    # Instance Methods
        
    def update_average_dog_count(self):
        """Update the average dog count based on all reports"""
        reports = self.dog_count_reports.all()
        if reports.exists():
            total_count = sum(report.count for report in reports)
            self.average_dog_count = round(total_count / reports.count(), 1)
        else:
            self.average_dog_count = 0
        self.save(update_fields=['average_dog_count'])

    def report_dog_count(self, user, count):
        """Record a new dog count report and update the average
        Move to user profile?
        """
        LocationDogCountReport.objects.create(
            location=self,
            user=user,
            count=count
        )
        self.update_average_dog_count()

    def update_crowd_meter(self):
        """Update the average crowd meter based on recent reports"""
        recent_reports = self.crowd_meter_reports.filter(
            reported_at__gte=timezone.now() - timedelta(hours=24)
        )
        if recent_reports.exists():
            total_value = sum(report.value for report in recent_reports)
            self.average_crowd_meter = round(total_value / recent_reports.count(), 1)
        else:
            self.average_crowd_meter = None
        self.save(update_fields=['average_crowd_meter'])

    def report_crowd_meter(self, user, value):
        """Record a new crowd meter report and update the average"""
        LocationCrowdMeter.objects.create(
            location=self,
            user=user,
            value=value
        )
        self.update_crowd_meter()

    @classmethod
    def get_or_create_by_coordinates(cls, latitude, longitude, city=None, region=None, max_distance=0.001):
        """
        Get or create a location based on coordinates.
        max_distance represents the maximum distance in decimal degrees 
        (roughly 100m at 0.001)
        """
        nearby_location = cls.objects.filter(
            latitude__range=(float(latitude) - max_distance, float(latitude) + max_distance),
            longitude__range=(float(longitude) - max_distance, float(longitude) + max_distance)
        ).first()

        if nearby_location:
            return nearby_location, False

        return cls.objects.create(
            latitude=latitude,
            longitude=longitude,
            city=city,
            region=region
        ), True