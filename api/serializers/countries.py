# -*- coding: utf-8 -*-
"""
countries serializers
"""
from rest_framework import serializers

from api.models import Country


class CountrySerializer(serializers.ModelSerializer):
    """
    Country serializer
    """
    class Meta:
        model = Country
        fields = '__all__'
