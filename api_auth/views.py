import requests
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from djoser.conf import settings as djoser

from api_auth.serializers import ContactSerializer
# from api_auth.models import Contact

from utils import get_user_models

_, Contact = get_user_models()


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def email_user_activation(request, uid, token):
    """ Confirm the email address. """

    # post_url = "http://127.0.0.1:8000/api/v1/auth/users/activation/"

    full_path = request.path.split("/")
    path_len = len(full_path) - 2
    path = [chunk for i, chunk in enumerate(full_path) if i < path_len]
    post_url = "http://" + request.get_host() + "/".join(path) + "/"
    post_data = {"uid": uid, "token": token}
    response = requests.post(post_url, data=post_data)
    resp = {"is_activated": False}
    try:
        resp += response.json()
    except Exception:
        resp["is_activated"] = True
        resp["detail"] = "Email is confirmed."
    return Response(resp, status=response.status_code)


class ContactViewSet(ModelViewSet):
    """ CRUD contacts """

    serializer_class = ContactSerializer
    permission_classes = djoser.PERMISSIONS.user
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Contact.objects.filter(to_user_id=self.request.user.id).all()
        # pprint(contact for contact in queryset if contact)
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get(pk=self.request.data['id'])
        except Exception:
            raise ValidationError('Contact id was not found')

        self.check_object_permissions(self.request, obj)
        return obj
