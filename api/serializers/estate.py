# -*- coding: utf-8 -*-
"""
Hotels serializers
"""
from rest_framework import serializers

from api.models import Hotel, Room, Address, City
from api.serializers.locations import AddressSerializer


class HotelRoomSerializer(serializers.ModelSerializer):
    """
    Room serializer
    """
    class Meta:
        model = Room
        fields = ['pk', 'price']


class HotelSerializer(serializers.ModelSerializer):
    """
    Hotel serializer
    """
    address = AddressSerializer()

    class Meta:
        model = Hotel
        fields = ['pk', 'name', 'rating', 'address']
        depth = 3
        extra_kwargs = {'rating': {"read_only": True}}

    def create(self, validated_data):
        """
        Custom create method
        """
        # retrieving info
        address_data = validated_data.pop('address')
        city_data = address_data.pop('city')
        if city_data.get('city_id'):
            city_id = city_data['city_id']
        else:
            city = City.objects.create(name=city_data['new_city'],
                                       country_id=city_data['country_id'])
            city_id = city.id
        address = Address.objects.create(**address_data, city_id=city_id)
        hotel = Hotel.objects.create(**validated_data, address=address)
        return hotel


class HotelRetrieveSerializer(HotelSerializer):
    """
    Hotel retrieve serializer
    """
    rooms = HotelRoomSerializer(many=True, read_only=True)

    class Meta(HotelSerializer.Meta):
        fields = HotelSerializer.Meta.fields + ['rooms']


class RoomSerializer(serializers.ModelSerializer):
    """
    Room serializer
    """
    hotel = HotelSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['pk', 'number', 'description', 'floor', 'price', 'hotel']
