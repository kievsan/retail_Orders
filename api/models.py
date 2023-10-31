from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from api_auth.models import Contact
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


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('shop name'), unique=True)
    url = models.URLField(verbose_name='url', null=True, blank=True)

    accepts_orders = models.BooleanField(verbose_name=_('store accepts orders'), default=True)

    class Meta:
        db_table = 'shops'
        verbose_name = _('Shop')
        verbose_name_plural = _('Shops')
        ordering = ('-name',)

    def __str__(self):
        return f'{self.name}'

    def category_list(self):
        return self.categories.all()

    def category_names_str(self):
        return ', '.join([category.name for category in self.categories.all()])


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name=_('category name'))
    shops = models.ManyToManyField(Shop, verbose_name=_('shops'),
                                   related_name='categories',
                                   blank=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('-name',)

    def __str__(self):
        return self.name

    def store_list(self):
        return self.shops.all()

    def store_names_str(self):
        return ', '.join([shop.name for shop in self.shops.all()])


class Product(models.Model):
    name = models.CharField(max_length=80, verbose_name=_('product name'))
    category = models.ForeignKey(Category, verbose_name=_('category'),
                                 related_name='products',
                                 blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductDetails(models.Model):
    external_id = models.PositiveIntegerField(verbose_name=_('external id'))
    product = models.ForeignKey(Product, verbose_name=_('product'),
                                related_name='product_details',
                                blank=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name=_('shop'),
                             related_name='product_details',
                             blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_('price'),
                                validators=[MinValueValidator(0)])
    rr_price = models.DecimalField(max_digits=20, decimal_places=2,
                                   verbose_name=_('recommended retail price'),
                                   validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'product_details'
        verbose_name = _('Product details')
        verbose_name_plural = _('Products details')
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop', 'external_id'],
                                    name='unique_product_details'),
        ]

    def __str__(self):
        return f'{self.shop}: {self.product}'


class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name=_('name'), unique=True)

    class Meta:
        db_table = 'parameters'
        verbose_name = _('Parameter name')
        verbose_name_plural = _('Parameter names')
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_details = models.ForeignKey(ProductDetails, verbose_name=_('product details'),
                                        related_name='product_parameters',
                                        blank=True, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name=_('parameter'),
                                  related_name='product_parameters',
                                  blank=True, on_delete=models.CASCADE)
    value = models.CharField(verbose_name=_('value'), max_length=100)

    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')
        constraints = [
            models.UniqueConstraint(fields=['product_details', 'parameter'],
                                    name='unique_product_parameter'),
        ]

    def __str__(self):
        return f'{self.value} ]'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             related_name='orders', blank=True,
                             on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField(verbose_name=_('status'), choices=STATE_CHOICES, max_length=25)
    contact = models.ForeignKey(Contact, verbose_name=_('contact'),
                                related_name='orders',
                                blank=True, null=True,
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('-dt',)
        constraints = [
            models.UniqueConstraint(fields=['user', 'dt'], name='unique_order'),
        ]

    def __str__(self):
        return f'{self.user} [ {self.dt} ]'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order'),
                              related_name='ordered_items',
                              blank=True, on_delete=models.CASCADE)
    product_details = models.ForeignKey(ProductDetails, verbose_name=_('prodict details'),
                                     related_name='ordered_items',
                                     blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))

    class Meta:
        verbose_name = _('Order position')
        verbose_name_plural = _('Order positions')
        constraints = [
            models.UniqueConstraint(fields=['order', 'product_details'],
                                    name='unique_order_item'),
        ]

    def __str__(self):
        return f'{self.order} / {self.product_details} / {self.quantity}'
