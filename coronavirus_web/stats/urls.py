from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('download_current', download_current)
]