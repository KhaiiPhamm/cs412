"""
    File: urls.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 11/13/2026
    Description: Joke and Picture urls
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('', RandomJokeView.as_view(), name='show_random'),
    path('random', RandomJokeView.as_view(), name='show_random'),
    path('jokes', JokeListView.as_view(), name='show_all_jokes'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='show_joke'),
    path('pictures', PictureListView.as_view(), name='show_all_pictures'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='show_picture'),
    
    path('api/', RandomJokeAPIView.as_view()),
    path('api/random', RandomJokeAPIView.as_view()),
    path('api/jokes', JokeListAPIView.as_view()),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view()),
    path('api/pictures', PictureListAPIView.as_view()),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view()),
    path('api/random_picture', RandomPictureAPIView.as_view()),    
]