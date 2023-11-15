from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Store


class UrlSerializer(serializers.ModelSerializer):
    url = serializers.URLField()


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        # fields = tuple(Store.REQUIRED_FIELDS)
        # read_only_fields = ('id',)
