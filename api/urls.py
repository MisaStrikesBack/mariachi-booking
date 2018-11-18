# -*- coding: utf-8 -*-
"""
api urls
"""
from django.urls import path, include

from api.utils import api_router
from api.views import SignOutView, SignUpView, SignInView, UpdatePasswordView

app_name = "api"

auth_patterns = ([
    path('signout/', SignOutView.as_view(), name='signout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('update/', UpdatePasswordView.as_view(), name='update'),
], 'auth')

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(api_router.urls)),
]
