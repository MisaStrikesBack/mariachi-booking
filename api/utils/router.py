# -*- coding: utf-8 -*-
"""
api viewset router
"""
from rest_framework.routers import SimpleRouter

from api.views import CountryListView

api_router = SimpleRouter()

api_router.register(
    r'country', CountryListView, base_name='country')
