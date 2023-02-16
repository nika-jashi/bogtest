from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from apps.accounts.models import CustomAccount

from apps.utils.custom_validators import (not_contains_symbols,
                                          not_contains_whitespace,
                                          contains_uppercase,
                                          contains_digits,
                                          contains_lowercase)


class AccountRegistrationSerializer(serializers.ModelSerializer):
    """A serializer for creating new users. Includes all the required
       fields and validations, plus a repeated password. """

    password = serializers.CharField(max_length=255, write_only=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=56, validators=[not_contains_symbols])
    last_name = serializers.CharField(max_length=56, validators=[not_contains_symbols])

    class Meta:
        model = CustomAccount
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": _("Those Passwords Don't Match.")})

        del data['confirm_password']  # deleting confirm_password because we don't use it after validation

        return data

    def create(self, validated_data):
        instance = CustomAccount.objects.create_user(**validated_data)
        return instance
