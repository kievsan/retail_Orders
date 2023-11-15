from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task
from yaml import load as yaml_load, SafeLoader
import requests

from api.models import Store, Category, Product, ProductDetails, Parameter, ProductParameter
from retail_orders.celery import app


@app.task
def celery_upload_partner_price(url=None, file_obj=None, user_id=0):
    """
    partner price list update (file/url)
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

        product_info = ProductDetails.objects.create(product_id=product.id,
                                                     external_id=item['id'],
                                                     price=item['price'],
                                                     rr_price=item['price_rrc'],
                                                     quantity=item['quantity'],
                                                     store_id=store.id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_info_id=product_info.id,
                                            parameter_id=parameter_object.id,
                                            value=value)


@shared_task()
def send_activation_email_example(email, token):
    """Send activation email"""
    subject = 'Welcome to Celery'
    message = 'Hope it helps me'
    sender = settings.EMAIL_FROM
    recipient_list = [email]
    html_message = '<h1>The End</h1>'
    send_mail(subject, message, sender, recipient_list, html_message=html_message)
