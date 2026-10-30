"""
    File: urls.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 10/30/2026
    Description: URL configuration for the voter_analytic app. Maps the profile [list/detail] view to their corresponding view functions.
"""
from django.urls import path
from . import views

urlpatterns = [
    # map the URL (empty string) to the view
    path(r'', views.VotersListView.as_view(), name='voters'),
    path(r'voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
    path(r'graphs', views.GraphsListView.as_view(), name='graphs'),
]