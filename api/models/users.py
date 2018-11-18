# -*- coding: utf-8 -*-
"""
Users custom models
"""
from django.db import models

from django.conf import settings

from api.models.estate import Hotel


class Group(models.Model):
    """
    User groups model
    """
    name = models.CharField(max_length=30)


class UserProfile(models.Model):
    """
    User aditional information
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True,
                                on_delete=models.CASCADE,
                                related_name='user_profile')
    phone = models.CharField(max_length=80,
                             null=True,
                             blank=True)
    group = models.ForeignKey(Group,
                              related_name='users',
                              on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel,
                              related_name='users',
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
