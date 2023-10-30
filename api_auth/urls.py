from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import email_user_activation, ContactViewSet

router = DefaultRouter()
router.register('contacts', ContactViewSet, basename='user_contacts')

urlpatterns = [
    path('users/activation/<str:uid>/<str:token>',
         email_user_activation, name='users-activation'),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
