from django.db import models

# Create your models here.

class ReviewModel(models.Model):
    author       = models.CharField(max_length=50)
    title        = models.CharField(max_length=250)
    body         = models.TextField()
    rating       = models.PositiveIntegerField(null=True)
    createdAt    = models.DateTimeField(auto_now_add=True)
