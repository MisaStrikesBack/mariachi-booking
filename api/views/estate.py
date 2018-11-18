# -*- coding: utf-8 -*-
"""
hotels services views
"""
from rest_framework import mixins, viewsets

from api.models import Hotel, Room
from api.constants import HOTEL_FILTERS_DICT
from api.utils.permissions import CreateIfHotelStaff
from api.serializers import (
    HotelSerializer, HotelRetrieveSerializer, RoomSerializer)


class HotelViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """
    Hotel view set
    """
    permission_classes = (CreateIfHotelStaff, )

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
                  viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
