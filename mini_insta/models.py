"""
    File: models.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 9/30/2026
    Description: Stores each user's profile information and 
    maps those fields to database columns
"""
from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    
    # data artibutes of Profile
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=False)
    join_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        """Return a string representation of this user"""
        return f'{self.username}'
    
    def get_all_posts(self):
        """Return all of the posts made by this user."""
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts
        
    def get_absolute_url(self):
        """Return the URL to view this post."""
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_followers(self):
        """Return all of the profiles that follow this user."""
        followers = Follow.objects.filter(profile=self)
        return [f.follower_profile for f in followers]
    
    def get_num_followers(self):
        """Return the number of followers this user has."""
        return len(self.get_followers())
    
    def get_following(self):
        """Return all of the profiles that this user follows."""
        following = Follow.objects.filter(follower_profile=self)
        return [f.profile for f in following]

    def get_num_following(self):
        """Return the number of profiles this user follows."""
        return len(self.get_following())
    
    def get_post_feed(self):
        """Return all of the posts made by this user and the users they follow."""
        following = self.get_following()
        posts = Post.objects.none()
        for profile in following:
            profile_posts = Post.objects.filter(profile=profile)
            posts = posts.union(profile_posts)
        return posts.order_by('-timestamp')        
        
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
    
    def get_all_comments(self):
        """Return all of the comments associated with this post."""
        comments = Comment.objects.filter(post=self).order_by('-timestamp')
        return comments
    
    def get_likes(self):
        """Return all of the likes associated with this post."""
        likes = Like.objects.filter(post=self)
        return likes
    
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
    
class Follow(models.Model):
    """
    Model the data attributes of a follow relationship between two users
    """
    
    # data attributes of Follow
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='profile')
    follower_profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='follower_profile')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """Return a string representation of this follow relationship."""
        return f'{self.follower_profile.username} follows {self.profile.username}'
    
class Comment(models.Model):
    """
    Model the data attributes of a comment on a post
    """
    
    # data attributes of Comment
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)
    
    def __str__(self):
        """Return a string representation of this comment."""
        return f'Comment by {self.profile.username} on {self.post} at {self.timestamp}'
    
class Like(models.Model):
    """
    Model the data attributes of a like on a post
    """
    
    # data attributes of Like
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """Return a string representation of this like."""
        return f'Like by {self.profile.username} on {self.post} at {self.timestamp}'