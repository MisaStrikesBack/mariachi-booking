# -*- coding: utf-8 -*-
"""
Auth views
"""
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from rest_framework import exceptions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from api.serializers import (SignInSerializer,
                             SignUpSerializer,
                             UpdatePasswordSerializer)


class SignInView(APIView):
    """
    SignIn view
    """
    serializer_class = SignInSerializer

    def post(self, request):
        """
        POST method
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password'])
        if not user:
            raise exceptions.AuthenticationFailed(
                'Login failed: Wrong credentials')

        # setting user login data
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        if settings.DEBUG:
            login(request, user)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'id': user.pk,
                         'user': user.get_full_name(),
                         'token': token.key})


class SignOutView(APIView):
    """
    SignOut view
    """
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        """
        post method
        """
        key = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]

        if settings.DEBUG and key == '':
            logout(request)
            return Response()
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise exceptions.APIException(
                "Invalid request",
                status.HTTP_400_BAD_REQUEST
            )
        token.delete()
        return Response("Successful logout")


class SignUpView(APIView):
    """
    SignUp view
    """
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdatePasswordView(APIView):
    """
    UpdatePassword view
    """
    serializer_class = UpdatePasswordSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.check_password(
                serializer.validated_data['current_password']):
            request.user.set_password(
                serializer.validated_data['new_password'])
            request.user.save()
            return Response(
                "Password successfully updated", status=status.HTTP_200_OK)
        raise exceptions.APIException(
            "Please submit the correct current password",
            status.HTTP_400_BAD_REQUEST
        )
