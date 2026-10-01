"""
    File: views.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 9/30/2026
    Description: View functions for the mini_insta app. Handles ProfileListView 
    and ProfileDetailView functions with corressponding attributes 
"""
from django.shortcuts import render

# Create your views here.
from .models import Profile
from django.views.generic import ListView, DetailView
 
class ProfileListView(ListView):
    '''Create a subclass of ListView to display all users.'''

    model = Profile 
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = 'profiles'
    
class ProfileDetailView(DetailView):
    '''Show the details for one user.'''
    
    model = Profile
    template_name="mini_insta/show_profile.html"
    context_object_name = 'profile'

