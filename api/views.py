from pprint import pprint

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import load as yaml_load

from rest_framework import viewsets, status
from rest_framework import serializers as drf_serializers
from rest_framework.permissions import IsAuthenticated

from api.models import Store
import api.serializers as serializers


class MeStoresViewSet(viewsets.ModelViewSet):
    """ CRUD for user's shops """
    permission_classes = [IsAuthenticated]
    # serializer_class = serializers.StoreSerializer

    def get_queryset(self):
        queryset = Store.objects.filter(to_user_id=self.request.user.id).all()
        # pprint(store for store in queryset if store)  ###
        return queryset

    # def get_object(self):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     pprint(data for data in self.request.data)  ###
    #     store_id = self.request.data.get('id')
    #     try:
    #         obj = queryset.get(pk=store_id)
    #     except Exception:
    #         raise ValidationError(f'Store ID={store_id} was not found')
    #
    #     self.check_object_permissions(self.request, obj)
    #     return obj

    def get_serializer_class(self):
        return serializers.StoreSerializer

    def create(self, request, *args, **kwargs):
        request.data['to_user'] = self.request.user.id
        # super().create(self, request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    filterset_fields = ('accepts_orders',)
    ordering_fields = ('name', 'id',)
    search_fields = ('name',)
    ordering = ('name',)


class PartnersStoresViewSet(viewsets.ReadOnlyModelViewSet):
    """ Partners stores list """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.StoreSerializer
    queryset = Store.objects.all()

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
