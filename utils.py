#
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_user_models():
    """
    Return the User and Contact models that is active in this project.
    """
    try:
        return apps.get_model(settings.AUTH_USER_MODEL, require_ready=False), \
               apps.get_model(settings.AUTH_USER_CONTACT_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL and AUTH_USER_CONTACT_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL or AUTH_USER_CONTACT_MODEL refers to model '%s' or '%s' that has not been installed"
            % settings.AUTH_USER_MODEL, settings.AUTH_USER_CONTACT_MODEL
        )
