from django.db import models
from django.utils.translation import gettext_lazy as _

from retail_orders import settings

STATE_CHOICES = (
    ('basket', _('Basket')),
    ('new', _('New')),
    ('confirmed', _('Confirmed')),
    ('assembled', _('Assembled')),
    ('sent', _('Sent')),
    ('delivered', _('Delivered')),
    ('canceled', _('Canceled')),
)



