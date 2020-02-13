# -*- coding: utf-8 -*-
from django.urls import path
from .views import get_conversion_api_view


urlpatterns = [
    path('convert/', get_conversion_api_view),
]