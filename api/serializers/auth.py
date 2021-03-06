# -*- coding: utf-8 -*-
"""
Authentication serializers
"""
from django.contrib.auth.models import User

from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from api.models import Group, UserProfile
from api.error_messages import (
    INCLUDE_EMAIL, SHORTER_EMAIL, VALID_EMAIL, SUBMIT_PASSWORD, VALID_PASSWORD,
    EMAIL_IN_USE, INVALID_GROUP, UNMATCHING_PASSWORDS)


class SignInSerializer(serializers.Serializer):
    """
    Sign In serializer
    """
    email = serializers.EmailField(
        max_length=60,
        error_messages={
            'required': INCLUDE_EMAIL,
            'blank': INCLUDE_EMAIL,
            'max_length': SHORTER_EMAIL,
            'invalid': VALID_EMAIL
        }
    )
    password = serializers.CharField(
        min_length=4,
        max_length=40,
        error_messages={
            'required': SUBMIT_PASSWORD,
            'blank': VALID_PASSWORD
        }
    )


class SignUpSerializer(serializers.ModelSerializer):
    """
    Sign Up serializer
    """
    group = serializers.IntegerField(max_value=99,
                                     write_only=True)
    phone = serializers.CharField(max_length=20,
                                  write_only=True,
                                  required=False)
    password = serializers.CharField(max_length=30,
                                     style={'input_type': 'password'},
                                     write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'phone', 'group', 'password')

    def validate_email(self, value):
        """
        email validator
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(EMAIL_IN_USE)
        return value

    def validate_group(self, value):
        """
        Group validator
        """
        if not Group.objects.filter(pk=value).exists():
            raise serializers.ValidationError(INVALID_GROUP)
        return value

    def create(self, validated_data):
        """
        Create method for SignUp Serializer
        """
        try:
            # creating the new user
            new_user = User(
                username=validated_data['email'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                is_active=True)

            new_user.set_password(validated_data['password'])
            new_user.save()
            # creating user profile
            UserProfile.objects.create(
                user=new_user,
                phone=validated_data['phone'],
                group_id=validated_data['group'])
            return new_user
        except Exception as e:
            raise APIException(
                e,
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdatePasswordSerializer(serializers.Serializer):
    """
    ResetPasswordSerializer class
    """
    new_password = serializers.CharField(min_length=6, max_length=20,
                                         style={'input_type': 'password'})
    confirm_password = serializers.CharField(min_length=6, max_length=20,
                                             style={'input_type': 'password'})
    current_password = serializers.CharField(min_length=6, max_length=20,
                                             style={'input_type': 'password'})

    def validate_new_password(self, value):
        if (self.initial_data['new_password'] ==
                self.initial_data['confirm_password']):
            return value
        raise serializers.ValidationError(UNMATCHING_PASSWORDS)
