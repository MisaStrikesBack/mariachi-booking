# -*- coding: utf-8 -*-
"""
api urls
"""
from django.urls import path, include

from api.utils import api_router

app_name = "api"

urlpatterns = [
    path('', include(api_router.urls)),
]
