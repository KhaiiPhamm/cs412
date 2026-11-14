"""
    File: models.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 11/13/2026
    Description: Joke and Picture model
"""
from django.db import models

# Create your models here.
class Joke (models.Model):
    """A joke class"""
    
    text = models.TextField(blank=False)
    name = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Dadjoke by {self.name}"

class Picture (models.Model):
    """A picture class"""
    
    image_url = models.URLField(blank=False)
    name = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name}"