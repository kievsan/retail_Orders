from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Store


class UrlSerializer(serializers.Serializer):
    url = serializers.URLField()


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = tuple(Store.REQUIRED_FIELDS)
        # fields = '__all__'
        # read_only_fields = ('id')


class StoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
