"""
    File: views.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 11/13/2026
    Description: Joke and Picture views
"""
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Joke, Picture
import random
from rest_framework import generics
from .serializers import JokeSerializer, PictureSerializer
# Create your views here.

class JokeListView(ListView):
    """A class for list of jokes"""
    
    model = Joke
    template_name = 'dadjokes/show_all_jokes.html'
    context_object_name = 'jokes'
    
class JokeDetailView(DetailView):
    """A class for detail of joke"""
    
    model = Joke
    template_name = 'dadjokes/show_joke.html'
    context_object_name = 'joke'
        
        
class PictureListView(ListView):
    """A class for list of pictures"""
    
    model = Picture
    template_name = 'dadjokes/show_all_pictures.html'
    context_object_name = 'pictures'
    
class PictureDetailView(DetailView):
    """A class for detail of picture"""
    
    model = Picture
    template_name = 'dadjokes/show_picture.html'
    context_object_name = 'picture'
    
class RandomJokeView(TemplateView):
    """A class to show one random Joke and one random Picture."""

    template_name = 'dadjokes/show_random.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['joke'] = random.choice(Joke.objects.all())
        context['picture'] = random.choice(Picture.objects.all())
        return context

class JokeListAPIView(generics.ListCreateAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class RandomJokeAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JokeSerializer

    def get_object(self):
        return random.choice(Joke.objects.all())

class PictureListAPIView(generics.ListAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomPictureAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PictureSerializer

    def get_object(self):
        return random.choice(Picture.objects.all())