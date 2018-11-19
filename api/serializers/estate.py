# -*- coding: utf-8 -*-
"""
Hotels serializers
"""
from rest_framework import serializers

from api.models import (
    Hotel, Room, Address, City, Amenity, AmenityType, Bed, BedType,
    AmenityType)
from api.serializers.locations import AddressSerializer
from api.error_messages import INVALID_BED_TYPE_ID, INVALID_AMENITY_TYPE_ID


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


class AmenitySerializer(serializers.ModelSerializer):
    """
    Room amenity serializer
    """
    class Meta:
        model = Amenity
        fields = ['pk', 'amenity_type', 'room']


class AmenityTypeSerializer(serializers.ModelSerializer):
    """
    Amenity info serializer
    """
    class Meta:
        model = AmenityType
        fields = ['pk', 'name', 'description']


class RoomAmenitySerializer(serializers.ModelSerializer):
    """
    Amenities serializer
    """
    amenity_type = AmenityTypeSerializer(read_only=True)

    class Meta:
        model = Amenity
        fields = ['pk', 'amenity_type']


class BedSerializer(serializers.ModelSerializer):
    """
    Room bed serializer
    """
    class Meta:
        model = Bed
        fields = ['pk', 'bed_type', 'room']


class BedTypeSerializer(serializers.ModelSerializer):
    """
    Bed info serializer
    """
    class Meta:
        model = BedType
        fields = ['pk', 'name', 'capacity']


class RoomBedSerializer(serializers.ModelSerializer):
    """
    Room bed serializer
    """
    bed_type = BedTypeSerializer(read_only=True)

    class Meta:
        model = Bed
        fields = ['pk', 'bed_type']


class RoomBedTypeCreationSerializer(serializers.Serializer):
    """
    Generic serializer to validate bedtype ids
    """
    new_beds = serializers.ListField()

    def validate_new_beds(self, value):
        """
        Validating new room beds
        """
        # returning all pk from bedtype
        bed_types_ids = set(BedType.objects.all().values_list('pk', flat=True))
        invalid_ids = set(value) - bed_types_ids
        if invalid_ids:
            raise serializers.ValidationError(INVALID_BED_TYPE_ID)
        return value


class RoomAmenityCreationSerializer(serializers.Serializer):
    """
    Generic serializer to validate amenitytype ids
    """
    new_amenities = serializers.ListField()

    def validate_new_amenities(self, value):
        """
        validating new room amenities
        """
        # returning all pk from bedtype
        amenity_type_ids = (
            set(AmenityType.objects.all().values_list('pk', flat=True)))
        invalid_ids = set(value) - amenity_type_ids
        if invalid_ids:
            raise serializers.ValidationError(INVALID_AMENITY_TYPE_ID)
        return value


class RoomSerializer(serializers.ModelSerializer):
    """
    Room serializer
    """
    hotel = HotelSerializer(read_only=True)
    amenities = RoomAmenitySerializer(many=True, read_only=True)
    beds = RoomBedSerializer(many=True, read_only=True)
    capacity = serializers.SerializerMethodField()
    # creation fields
    new_room_beds = RoomBedTypeCreationSerializer(write_only=True,
                                                  required=False)
    new_rom_amenities = RoomAmenityCreationSerializer(write_only=True,
                                                      required=False)

    class Meta:
        model = Room
        fields = ['pk', 'number', 'description', 'floor', 'price', 'hotel',
                  'amenities', 'beds', 'capacity', 'new_room_beds',
                  'new_rom_amenities']

    def get_capacity(self, obj):
        return obj.get_capacity()

    def create(self, validated_data):
        """
        custom creation method
        """
        # getting beds type ids
        beds = validated_data.pop('new_room_beds')
        # getting amenities type ids
        amenities = validated_data.pop('new_rom_amenities')
        # creating the new room instance
        validated_data['hotel_id'] = (
            self.context['request'].user.user_profile.hotel.id)
        room = Room.objects.create(**validated_data)
        # creating the beds relations
        for bed_id in beds['new_beds']:
            Bed.objects.create(bed_type_id=bed_id, room=room)
        # creating the amenities relations
        for amenity_id in amenities['new_amenities']:
            Amenity.objects.create(amenity_type_id=bed_id, room=room)
        return room
