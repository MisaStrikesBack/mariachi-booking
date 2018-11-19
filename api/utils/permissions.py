# -*- coding: utf-8 -*-
"""
api permission classes
"""
from rest_framework import permissions


class CreateUpdateIfHotelStaff(permissions.BasePermission):
    """
    hotel staff user is able to create a new instance
    """
    def has_permission(self, request, view):
        if (view.action in ['create', 'update'] and
                (not request.user.is_authenticated or
                 request.user.user_profile.group_id != 1)):
            return False
        return True


class DestroyIfHotelStaff(permissions.BasePermission):
    """
    Allows delete instance only if hotel staff user
    """
    def has_permission(self, request, view):
        if (request.method == "DELETE" and
                (not request.user.is_authenticated or
                 request.user.user_profile.group_id != 1)):
            return False
        return True


class IsCustomer(permissions.BasePermission):
    """
    Checks if the request was made by a customer user
    """
    def has_permission(self, request, view):
        if (not request.user.is_authenticated or
                request.user.user_profile.group_id != 2):
            return False
        return True
