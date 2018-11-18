# -*- coding: utf-8 -*-
"""
country services views
"""
from rest_framework import mixins, viewsets

from api.models import Country
from api.serializers import CountrySerializer
from api.utils.custom_pagination import LargePagination


class CountryListView(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = LargePagination
