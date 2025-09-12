from django.db import models

# Create your models here.

class ReviewModel(models.Model):
    author       = models.CharField(max_length=50, null=True, blank=True)
    title        = models.CharField(max_length=250, null=True, blank=True)
    body         = models.TextField(null=True, blank=True)
    rating       = models.PositiveIntegerField(null=True, blank=True, default=0)
    added_at     = models.DateTimeField(auto_now_add=True)
    edited_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-added_at']