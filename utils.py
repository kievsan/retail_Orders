#
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from yaml import load as yaml_load, SafeLoader
import requests

from api.models import Store, Category, Product, ProductDetails, Parameter, ProductParameter


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


def upload_store_price(url=None, file_obj=None, user_id=0):
    """
    Store price list update (file/url)
    """
    if file_obj:
        data = yaml_load(file_obj, Loader=SafeLoader)
    else:
        stream = requests.get(url).content
        data = yaml_load(stream, Loader=SafeLoader)

    store, _ = Store.objects.get_or_create(name=data.get('store'), defaults={'owner_id': user_id})

    for category in data['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.stores.add(store.id)
        category_object.save()

    ProductDetails.objects.filter(store_id=store.id).delete()

    for item in data['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

        product_detail = ProductDetails.objects.create(product_id=product.id,
                                                       external_id=item['id'],
                                                       price=item['price'],
                                                       rr_price=item['price_rrc'],
                                                       quantity=item['quantity'],
                                                       store_id=store.id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_detail_id=product_detail.id,
                                            parameter_id=parameter_object.id,
                                            value=value)
