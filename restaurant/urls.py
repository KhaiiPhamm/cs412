"""
    File: urls.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 9/23/2026
    Description: URL configuration for the restaurant app. Maps the main landing page,
    order page, and confirmation page to their corresponding view functions.
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),           # cs-webapps.bu.edu/khaipduc/main/
    path(r'order/',views.order, name="order"),
    path(r'confirmation/', views.confirmation, name = "confirmation"),
]