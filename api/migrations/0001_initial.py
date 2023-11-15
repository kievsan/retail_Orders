# Generated by Django 4.2.6 on 2023-11-15 10:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_auth', '0002_remove_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='category name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(choices=[('basket', 'Basket'), ('new', 'New'), ('confirmed', 'Confirmed'), ('assembled', 'Assembled'), ('sent', 'Sent'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], max_length=25, verbose_name='status')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api_auth.contact', verbose_name='contact')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('-dt',),
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Parameter name',
                'verbose_name_plural': 'Parameter names',
                'db_table': 'parameters',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='product name')),
                ('categories', models.ManyToManyField(blank=True, related_name='products', to='api.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'products',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='ProductDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.PositiveIntegerField(verbose_name='external id')),
                ('quantity', models.PositiveIntegerField(verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('rr_price', models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MinValueValidator(0)], verbose_name='recommended retail price')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_details', to='api.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Product details',
                'verbose_name_plural': 'Products details',
                'db_table': 'product_details',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='store name')),
                ('url', models.URLField(blank=True, null=True, verbose_name='url')),
                ('accepts_orders', models.BooleanField(default=True, verbose_name='store accepts orders')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stores', to=settings.AUTH_USER_MODEL, verbose_name='user name')),
            ],
            options={
                'verbose_name': 'Store',
                'verbose_name_plural': 'Stores',
                'db_table': 'stores',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='ProductParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100, verbose_name='value')),
                ('parameter', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_parameters', to='api.parameter', verbose_name='parameters')),
                ('product_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_parameters', to='api.productdetails', verbose_name='product detail')),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': 'Parameters',
            },
        ),
        migrations.AddField(
            model_name='productdetails',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_details', to='api.store', verbose_name='store'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='quantity')),
                ('order', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordered_items', to='api.order', verbose_name='order')),
                ('product_details', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordered_items', to='api.productdetails', verbose_name='products details')),
            ],
            options={
                'verbose_name': 'Order position',
                'verbose_name_plural': 'Order positions',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='stores',
            field=models.ManyToManyField(blank=True, related_name='categories', to='api.store', verbose_name='stores'),
        ),
        migrations.AddConstraint(
            model_name='productparameter',
            constraint=models.UniqueConstraint(fields=('product_detail', 'parameter'), name='unique_product_parameter'),
        ),
        migrations.AddConstraint(
            model_name='productdetails',
            constraint=models.UniqueConstraint(fields=('product', 'store', 'external_id'), name='unique_product_details'),
        ),
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.UniqueConstraint(fields=('order', 'product_details'), name='unique_order_item'),
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.UniqueConstraint(fields=('user', 'dt'), name='unique_order'),
        ),
    ]
