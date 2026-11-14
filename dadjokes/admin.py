from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Joke)
admin.site.register(Picture)
