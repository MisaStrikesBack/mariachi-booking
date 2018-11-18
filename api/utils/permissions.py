# -*- coding: utf-8 -*-
"""
api permission classes
"""
from rest_framework import permissions


class CreateIfHotelStaff(permissions.BasePermission):
    """
    hotel staff user is able to create a new instance
    """
    def has_permission(self, request, view):
        if (view.action == 'create' and
                (not request.user.is_authenticated or
                 request.user.user_profile.group_id != 1)):
            return False
        return True
