# -*- coding: utf-8 -*-
"""
hotels services views
"""
from rest_framework import mixins, viewsets

from api.models import Reservation
from api.serializers import ReservationSerializer


class ReservationViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """
    Reservation view set
    """
    serializer_class = ReservationSerializer

    def get_queryset(self):
        if self.request.user.user_profile.hotel:
            query = Reservation.objects.filter(
                room__hotel_id=self.request.user.user_profile.hotel.id)
        else:
            query = Reservation.objects.filter(user_id=self.request.user.id)
        return query
