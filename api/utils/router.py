# -*- coding: utf-8 -*-
"""
api viewset router
"""
from rest_framework.routers import SimpleRouter

from api.views import CountryListView, HotelViewSet, RoomViewSet

api_router = SimpleRouter()

api_router.register(
    r'countries', CountryListView, base_name='countries')

api_router.register(
    r'hotels', HotelViewSet, base_name='hotels')

api_router.register(
    r'rooms', RoomViewSet, base_name='hotels')
