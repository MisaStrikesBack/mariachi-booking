# -*- coding: utf-8 -*-
"""
Locations serializers
"""
from rest_framework import serializers

from api.models import Address, Country, City
from api.error_messages import (
    INVALID_COUNTRY_ID, NO_CITY_SUBMITTED, NO_COUNTRY_SUBMITTED,
    INVALID_CITY_ID)


class CountrySerializer(serializers.ModelSerializer):
    """
    Country Serializer
    """
    class Meta:
        model = Country
        fields = ['pk', 'name']


class CitySerializer(serializers.ModelSerializer):
    """
    City Serializer
    """
    country = CountrySerializer(read_only=True)
    country_id = serializers.IntegerField(write_only=True, required=False)
    city_id = serializers.IntegerField(write_only=True, required=False)
    new_city = serializers.CharField(max_length=50, write_only=True,
                                     required=False)

    class Meta:
        model = City
        fields = ['pk', 'name', 'country', 'country_id', 'city_id', 'new_city']
        extra_kwargs = {'name': {'read_only': True}}

    def validate(self, data):
        """
        Object level validation
        """
        if not data.get('city_id') and not data.get('new_city'):
            raise serializers.ValidationError(NO_CITY_SUBMITTED)
        if data.get('new_city') and not data.get('country_id'):
            raise serializers.ValidationError(NO_COUNTRY_SUBMITTED)
        return data

    def validate_country_id(self, value):
        """
        assessing id is a valid country id
        """
        if not Country.objects.filter(pk=value).exists():
            raise serializers.ValidationError(INVALID_COUNTRY_ID)
        return value

    def validate_city_id(self, value):
        """
        assessing id is a valid country id
        """
        if not City.objects.filter(pk=value).exists():
            raise serializers.ValidationError(INVALID_CITY_ID)
        return value


class AddressSerializer(serializers.ModelSerializer):
    """
    Address serializer
    """
    city = CitySerializer()

    class Meta:
        model = Address
        fields = ['pk', 'street', 'neighborhood', 'post_code', 'city']
