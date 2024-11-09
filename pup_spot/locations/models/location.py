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
    likes = models.ManyToManyField(User, related_name='liked_locations', blank=True)
    crowd_meter = models.FloatField(
        blank=True, 
        null=True, 
        help_text="Scale of 1-10"
    )
    ratings = models.ForeignKey(
        'Rating',
        on_delete=models.CASCADE,
        related_name='locations',
        blank=True,
        null=True
    )
    average_dog_count = models.IntegerField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

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

    ##
    # Instance Methods
        
    def add_like(self, user):
        """Add a like from a user"""
        if not self.likes.filter(id=user.id).exists():
            self.likes.add(user)
            return True
        return False

    def remove_like(self, user):
        """Remove a like from a user"""
        if self.likes.filter(id=user.id).exists():
            self.likes.remove(user)
            return True
        return False

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