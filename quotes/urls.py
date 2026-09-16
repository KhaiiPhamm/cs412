from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.quote, name='quote'),           # cs-webapps.bu.edu/khaipduc/quotes/
    path(r'quote/',views.quote, name="quote"),
    path(r'show_all/', views.show_all, name="show_all"),
    path(r'about/', views.about, name="about"),
]