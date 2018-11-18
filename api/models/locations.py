# -*- coding: utf-8 -*-
"""
Location models
"""
from django.db import models


class Country(models.Model):
    """
    Country model
    """
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)


class City(models.Model):
    """
    City model
    """
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country,
                                related_name='cities',
                                on_delete=models.CASCADE)


class Address(models.Model):
    """
    Address model
    """
    street = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=50)
    post_code = models.CharField(max_length=15)
    city = models.ForeignKey(City,
                             related_name='addresses',
                             on_delete=models.CASCADE)
