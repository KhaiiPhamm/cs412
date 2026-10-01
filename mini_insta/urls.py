"""
    File: urls.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 9/30/2026
    Description: URL configuration for the mini_insta app. Maps the profile [list/detail] view to their corresponding view functions.
"""
from django.urls import path
from .views import ProfileListView, ProfileDetailView
 
 
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"), 
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
]