from django.urls import path, include
from rest_framework.routers import DefaultRouter

import api.views as views

router = DefaultRouter()
router.register('stores/partners', views.PartnersStoresViewSet, basename='partners_stores')
router.register('stores/me', views.MeStoresViewSet, basename='me_stores')


urlpatterns = [
    path('', include(router.urls)),
]
