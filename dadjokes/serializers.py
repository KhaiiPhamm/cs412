"""
    File: serializers.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 11/13/2026
    Description: Joke and Picture serializaer
"""
from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    """ A serializer for the Joke model"""
    
    class Meta:
        model = Joke
        fields = ['text', 'name', 'timestamp']
        
    def create(self, validated_data):
        """Override the superclass method that handles object notation"""
        
        # create a Joke obj
        joke = Joke(**validated_data)
        # save the obj to the database
        joke.save()
        # return an obj instance
        return joke

class PictureSerializer(serializers.ModelSerializer):
    '''A serializer for the Picture model'''

    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'name', 'timestamp']
    