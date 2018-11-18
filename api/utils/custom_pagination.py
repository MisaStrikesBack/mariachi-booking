# -*- coding: utf-8 -*-
"""
api custom pagination clases
"""
from rest_framework.pagination import PageNumberPagination


class LargePagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
