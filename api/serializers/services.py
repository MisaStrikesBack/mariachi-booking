# -*- coding: utf-8 -*-
"""
services serializers
"""
from rest_framework import serializers

from api.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    """
    Reservation serializer
    """
    class Meta:
        model = Reservation
        fields = ['pk', 'room', 'checkin_date', 'checkout_date', 'status']

    def create(self, validated_data):
        """
        Custom creation method
        """
        reservation = (
            Reservation.objects.create(
                **validated_data, user_id=self.context['request'].user.id))
        return reservation
