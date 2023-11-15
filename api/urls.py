from django.urls import path, include
from rest_framework.routers import DefaultRouter

import api.views as views

router = DefaultRouter()
router.register('stores', views.StoreViewSet, basename='stores')
router.register('stores/partner', views.PartnersStoresViewSet, basename='partner_stores')
router.register('stores/me', views.MeStoresViewSet, basename='me_stores')


urlpatterns = [
    path('', include(router.urls)),
]
