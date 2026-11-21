from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    """A serializer for the Profile model"""
    
    class Meta: 
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date']
        
     
class PhotoSerializer(serializers.ModelSerializer):
    """A serializer for the Photo model"""
    
    url = serializers.SerializerMethodField()
    class Meta:
        model = Photo
        fields = ['id', 'post', 'timestamp', 'image_url', 'image_file', 'url']

    def get_url(self, object):
        if object.image_url:
            return object.image_url
        if object.image_file:
            request = self.context.get('request')
            return request.build_absolute_uri(object.image_file.url) if request else object.image_file.url
        return None
      
class PostSerializer(serializers.ModelSerializer):
    """A serializer for the Post model"""
    
    photos = PhotoSerializer(source='photo_set', many=True, read_only=True)
    profile_display_name = serializers.CharField(source='profile.display_name', read_only=True)

    class Meta: 
        model = Post
        fields = ['id', 'profile', 'profile_display_name','timestamp', 'caption', 'photos']
        read_only_fields = ['profile']
                     
class CommentSerializer(serializers.ModelSerializer):
    """A serializer for the Comment model"""
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'profile', 'timestamp', 'text']
        
class LikeSerializer(serializers.ModelSerializer):
    """A serializer for the Like model"""
    
    class Meta:
        model = Like
        fields = ['id', 'post', 'profile', 'timestamp']