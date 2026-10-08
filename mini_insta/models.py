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
    
    def get_all_posts(self):
        """Return all of the posts made by this user."""
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts
    
class Post(models.Model):
    """
    Model the data attributes of an Instagram post      
    """
    
    # data attributes of Post
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=False)
    
    def __str__(self):
        """Return a string representation of this post."""
        return f'Post by {self.profile.username} at {self.timestamp}'
    
    def get_all_photos(self):
        """Return all of the photos associated with this post."""
        photos = Photo.objects.filter(post=self)
        return photos
    
class Photo(models.Model):
    """
    Model the data attributes of an image associated with a Post
    """
    
    # data attributes of Photo
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    
    def __str__(self):
        """Return a string representation of this photo."""
        return f'Photo by {self.post.profile.username} at {self.timestamp} with URL {self.get_image_url()}'
    
    def get_image_url(self):
        '''Return the URL of the image: image_url if set, else the uploaded file's URL.'''
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ''