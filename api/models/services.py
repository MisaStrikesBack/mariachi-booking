# -*- coding: utf-8 -*-
"""
Services models
"""
from django.db import models
from django.contrib.auth.models import User

from api.constants import STATUS_OPTIONS
from api.models.estate import Hotel, Room


class Reservation(models.Model):
    """
    Reservation model
    """
    user = models.ForeignKey(User,
                             related_name='reservations',
                             on_delete=models.CASCADE)
    room = models.ForeignKey(Room,
                             related_name='reservations',
                             on_delete=models.CASCADE)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    comment = models.CharField(max_length=200,
                               null=True,
                               blank=True)
    status = models.CharField(max_length=2,
                              choices=STATUS_OPTIONS,
                              default='A')


class Comment(models.Model):
    """
    Hotel comments model
    """
    message = models.TextField(max_length=300)
    creation_date = models.DateTimeField()
    user = models.ForeignKey(User,
                             related_name='comments',
                             on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel,
                              related_name='comments',
                              on_delete=models.CASCADE)
