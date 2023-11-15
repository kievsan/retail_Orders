import os
from pprint import pprint

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import load as yaml_load

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from api.models import Store
import api.serializers as serializers
from api.responses import ResponseOK
from api.tasks import celery_upload_store_price


def viewset_info(veiwset, rout, current_user, target_user) -> str:
    return (f'performed Request({veiwset.basename}: {rout}, {veiwset.action}, '
            f'user_id:\t{current_user} -> {target_user})')


def validate_url(url):
    """
    url validator
    """
    serializer = serializers.UrlSerializer(data=url)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data.get('url')


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """ Any stores (stores/any) """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.StoreSerializer
    queryset = Store.objects.all()

    filterset_fields = ('accepts_orders',)
    ordering_fields = ('name', 'id',)
    search_fields = ('name',)
    ordering = ('name',)


class PartnersStoresViewSet(viewsets.ReadOnlyModelViewSet):
    """ Partner stores (stores/partner/)"""

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.StoreSerializer

    def get_queryset(self):
        current_user_id = self.request.user.id
        # target_user_id = self.request.parser_context['kwargs'].get('pk')
        target_user_id = current_user_id if self.action == 'list' else self.kwargs.get('pk')
        print(viewset_info(self, 'stores/partner/', current_user_id, target_user_id))  ###
        objects = Store.objects.filter(owner_id=target_user_id)
        queryset = objects.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        return super(PartnersStoresViewSet, self).list(self, request, *args, **kwargs)

    filterset_fields = ('accepts_orders',)
    ordering_fields = ('name', 'id',)
    search_fields = ('name',)
    ordering = ('name',)


class MeStoresViewSet(viewsets.ModelViewSet):
    """ CRUD for user's shops (stores/me/)"""

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        self.request.data['owner'] = self.request.data.get('owner', self.request.user.id)
        return serializers.StoreSerializer

    def get_queryset(self):
        current_user_id = self.request.user.id
        target_user_id = current_user_id
        print(viewset_info(self, 'stores/me/', current_user_id, target_user_id))  ###
        objects = Store.objects.filter(owner_id=target_user_id)
        queryset = objects.all()
        return queryset

    def partial_update(self, request, *args, **kwargs):
        price_list_url = self.request.data.get('price_list_url')
        if price_list_url:
            # price_list_url = validate_url(price_list_url)
            store_id = kwargs.get('pk')
            print(f'Файл для загрузки прайса магазина {store_id} ищем по маршруту:\tdata/{price_list_url}') ###
            celery_upload_store_price(None, price_list_url, None, request.user.id, store_id)
            return ResponseOK(message='the price list is being updated...')
        return viewsets.ModelViewSet.partial_update(self, request, *args, **kwargs)

    filterset_fields = ('accepts_orders',)
    ordering_fields = ('name', 'id',)
    search_fields = ('name',)
    ordering = ('name',)

# class PartnerUpdate(APIView):
#     """
#     Класс для обновления прайса от поставщика
#     """
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
#
#         if request.user.type != 'shop':
#             return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)
#
#         url = request.data.get('url')
#         if url:
#             validate_url = URLValidator()
#             try:
#                 validate_url(url)
#             except ValidationError as e:
#                 return JsonResponse({'Status': False, 'Error': str(e)})
#             else:
#                 stream = get(url).content
#
#                 data = load_yaml(stream, Loader=Loader)
#
#                 shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
#                 for category in data['categories']:
#                     category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
#                     category_object.shops.add(shop.id)
#                     category_object.save()
#                 ProductDetails.objects.filter(shop_id=shop.id).delete()
#                 for item in data['goods']:
#                     product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])
#
#                     product_info = ProductDetails.objects.create(product_id=product.id,
#                                                               external_id=item['id'],
#                                                               model=item['model'],
#                                                               price=item['price'],
#                                                               price_rrc=item['price_rrc'],
#                                                               quantity=item['quantity'],
#                                                               shop_id=shop.id)
#                     for name, value in item['parameters'].items():
#                         parameter_object, _ = Parameter.objects.get_or_create(name=name)
#                         ProductParameter.objects.create(product_info_id=product_info.id,
#                                                         parameter_id=parameter_object.id,
#                                                         value=value)
#
#                 return JsonResponse({'Status': True})
#
#         return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
