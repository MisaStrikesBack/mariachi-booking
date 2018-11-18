# -*- coding: utf-8 -*-
"""
Csrf authentication bypass for DEV use (Don not use in PRODUCTION)
"""

from rest_framework.authentication import SessionAuthentication


class NoCsrfSessionAuthentication(SessionAuthentication):
    """
    CSRF-disabling authenticator. Use it ONLY in DEV env
    """

    def enforce_csrf(self, request):
        # overwritting csfr check and bypassing it
        return
