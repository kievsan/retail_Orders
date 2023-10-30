# добавить Celery в проект
from .celery import app as celery_app

__all__ = ['celery_app']
