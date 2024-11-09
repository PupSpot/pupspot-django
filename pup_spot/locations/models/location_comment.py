from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LocationComment(models.Model):
    location = models.ForeignKey('locations.Location', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='location_comments')
    content = models.TextField()
    votes = models.ManyToManyField(User, related_name='comment_votes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} at {self.location}"