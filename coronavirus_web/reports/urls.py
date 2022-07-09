from django.urls import path

from .views import *

urlpatterns = [
    path('', report_page),
    path('create/', create_report),
]