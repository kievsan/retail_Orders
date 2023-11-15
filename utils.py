#
import os
from pprint import pprint

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from yaml import load as yaml_load, SafeLoader, safe_load
import requests

from api.models import Store, Category, Product, ProductDetails, Parameter, ProductParameter
from api.responses import ResponseOK


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


def upload_store_price(url=None, file_name=None, file_obj=None, user_id=0, store_id=0):
    """
    Store price list update (file/url)
    """
    result = 'SUCCESS'
    if file_name:
        path = os.path.join(os.getcwd())
        file_route = os.path.join(path, "data", file_name)
        try:
            with open(file_route, encoding='utf-8') as f:
                data = safe_load(f)
        except OSError as err:
            result = f'FAILURE:\n\t{err}'
        print(f'reading... {result}!')  ##############

    # if file_obj:
    #     data = yaml_load(file_obj, Loader=SafeLoader)
    # else:
    #     stream = requests.get(url).content
    #     data = yaml_load(stream, Loader=SafeLoader)

    pprint(data)

    #######     Store
    store, _ = Store.objects.get_or_create(
        name=data.get('shop'),
        defaults={'owner_id': user_id, 'store_id': store_id}
    )

    #######     Category
    for category in data['categories']:
        category_obj, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_obj.stores.add(store.id)
        category_obj.save()

    #######     ProductDetails
    ProductDetails.objects.filter(store_id=store.id).delete()

    #######     Product
    for item in data['goods']:
        product_obj, _ = Product.objects.get_or_create(name=item['name'])
        product_obj.categories.add(item['category'])
        product_obj.save()

        product_details = ProductDetails.objects.create(product_id=product_obj.id,
                                                        external_id=item['id'],
                                                        price=item['price'],
                                                        rr_price=item['price_rrc'],
                                                        quantity=item['quantity'],
                                                        store_id=store.id)
        for name, value in item['parameters'].items():
            parameter, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_detail_id=product_details.id,
                                            parameter_id=parameter.id,
                                            value=value)

    return ResponseOK(message='the price list is being updated...')
