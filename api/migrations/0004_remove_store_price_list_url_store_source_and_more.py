# Generated by Django 4.2.6 on 2023-11-16 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_items_store_product_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='price_list_url',
        ),
        migrations.AddField(
            model_name='store',
            name='source',
            field=models.URLField(blank=True, null=True, verbose_name='price list source'),
        ),
        migrations.AddField(
            model_name='store',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='price list update date'),
        ),
    ]
