from django.db import models

class BaseProfile(models.Model):
    display_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # avatar = models.ImageField() - We have to integrate this later

    class Meta:
        abstract = True