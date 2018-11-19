# -*- coding: utf-8 -*-
"""
hotels services views
"""
from rest_framework import mixins, viewsets

from api.models import Hotel, Room, Bed, Amenity
from api.constants import HOTEL_FILTERS_DICT
from api.utils.permissions import CreateUpdateIfHotelStaff, DestroyIfHotelStaff
from api.serializers import (
    HotelSerializer, HotelRetrieveSerializer, RoomSerializer, BedSerializer,
    AmenitySerializer)


class HotelViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """
    Hotel view set
    """
    permission_classes = (CreateUpdateIfHotelStaff, )

    def get_queryset(self):
        """
        Country and city filter
        """
        qs = Hotel.objects.all()
        filter = {}
        for key, value in self.request.query_params.items():
            if key in ['country', 'city']:
                filter[HOTEL_FILTERS_DICT[key]] = value
        return qs.filter(**filter)

    def get_serializer_class(self):
        """
        Serializer class selection
        """
        serializer = {
            'list': HotelSerializer,
            'create': HotelSerializer,
            'retrieve': HotelRetrieveSerializer}
        return serializer[self.action]


class RoomViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    Room viewset
    """
    permission_classes = (CreateUpdateIfHotelStaff, DestroyIfHotelStaff)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BedViewSet(mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """
    Bed creation and deletion viewset
    """
    permission_classes = (CreateUpdateIfHotelStaff, DestroyIfHotelStaff)
    serializer_class = BedSerializer

    def get_queryset(self):
        return Bed.objects.filter(
            room__hotel_id=self.request.user.user_profile.hotel.id)


class AmenityViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    Amenity creation and deletion viewset
    """
    permission_classes = (CreateUpdateIfHotelStaff, DestroyIfHotelStaff)
    serializer_class = AmenitySerializer

    def get_queryset(self):
        return Amenity.objects.filter(
            room__hotel_id=self.request.user.user_profile.hotel.id)
