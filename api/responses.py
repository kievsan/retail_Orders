from rest_framework.response import Response
from rest_framework import status as http_status


def ResponseBase(status, code, **kwargs):
    response = {'status': status}
    if kwargs:
        response.update(kwargs)
    return Response(response, status=code)


def ResponseOK(**kwargs):
    return ResponseBase(True, http_status.HTTP_200_OK, **kwargs)


def ResponseNotFound(**kwargs):
    return ResponseBase(False, http_status.HTTP_404_NOT_FOUND, **kwargs)


def ResponseBadRequest(**kwargs):
    return ResponseBase(False, http_status.HTTP_400_BAD_REQUEST, **kwargs)


#################################   Celery:

def CeleryResponseBase(task_id, status_code, **kwargs):
    response = {'task_id': task_id}
    if kwargs:
        response.update(kwargs)
    return Response(response, status=status_code)


def CeleryResponseOK(task_id, **kwargs):
    return CeleryResponseBase(task_id, http_status.HTTP_200_OK, **kwargs)
