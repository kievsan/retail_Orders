from rest_framework import serializers
import djoser.serializers as djoser
from djoser.conf import settings

from utils import get_user_models

User, Contact = get_user_models()


class UserSerializer(djoser.UserSerializer):
    """
    заменить в djoser:
        стандартный user (users/),
        current_user (users/me/)
    """
    class Meta:
        model = User
        fields = tuple(
            User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,) + (
            User.CONTACTS_DB,
        )
        depth = 1
        read_only_fields = (settings.LOGIN_FIELD, User.CONTACTS_DB,)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
