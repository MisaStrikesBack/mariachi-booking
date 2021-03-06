# -*- coding: utf-8 -*-
"""
hotel models
"""
from django.db import models

from api.models import Address


class Hotel(models.Model):
    """
    Hotel model
    """
    name = models.CharField(max_length=60)
    rating = models.DecimalField(max_digits=2,
                                 decimal_places=1,
                                 null=True,
                                 blank=True)
    address = models.ForeignKey(Address,
                                related_name='hotel',
                                on_delete=models.CASCADE)


class Room(models.Model):
    """
    Room model
    """
    number = models.CharField(max_length=30)
    description = models.TextField(max_length=250,
                                   null=True,
                                   blank=True)
    floor = models.CharField(max_length=35,
                             null=True,
                             blank=True)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2)
    hotel = models.ForeignKey(Hotel,
                              related_name='rooms',
                              on_delete=models.CASCADE)

    def __str__(self):
        return "{}, hotel: {}".format(self.number, self.hotel.name)

    def get_capacity(self):
        """
        Return the room capacity based in the beds
        """
        return sum(self.beds.all().values_list('bed_type__capacity',
                                               flat=True))


class BedType(models.Model):
    """
    Bed types model
    """
    name = models.CharField(max_length=30)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Bed(models.Model):
    """
    Bed model
    """
    bed_type = models.ForeignKey(BedType,
                                 related_name='beds',
                                 on_delete=models.CASCADE)
    room = models.ForeignKey(Room,
                             related_name="beds",
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.bed_type.name


class AmenityType(models.Model):
    """
    Amenity type model
    """
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=180,
                                   null=True,
                                   blank=True)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    """
    Amenity model
    """
    amenity_type = models.ForeignKey(AmenityType,
                                     related_name='amenities',
                                     on_delete=models.CASCADE)
    room = models.ForeignKey(Room,
                             related_name='amenities',
                             on_delete=models.CASCADE)
