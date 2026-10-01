"""
    File: models.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 9/30/2026
    Description: Stores each user's profile information and 
    maps those fields to database columns
"""
from django.db import models

# Create your models here.
class Profile(models.Model):
    
    # data artibutes of Profile
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=False)
    join_date = models.DateField(auto_now=True)
    
    def __str__(self):
        """Return a string representation of this user"""
        return f'{self.username}'