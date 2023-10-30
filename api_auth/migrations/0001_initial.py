# Generated by Django 4.2.6 on 2023-10-28 00:43

import api_auth.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='last name')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('patronymic', models.CharField(blank=True, max_length=30, verbose_name='patronymic')),
                ('company', models.CharField(blank=True, help_text='Enter company name', max_length=50, verbose_name='company')),
                ('position', models.CharField(blank=True, help_text='Enter staff position in company', max_length=50, verbose_name='position')),
                ('type', models.CharField(choices=[('shop', 'Shop'), ('buyer', 'Buyer')], default='buyer', max_length=10, verbose_name='user type')),
                ('username', models.CharField(blank=True, max_length=10, verbose_name='user name')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, help_text='Enter email address. Letters, digits and @/./+/-/_ only.', max_length=50, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='email address')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'users',
                'ordering': ('email',),
                'abstract': False,
            },
            managers=[
                ('objects', api_auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.CharField(blank=True, help_text='Enter contact person', max_length=50, verbose_name='contact person')),
                ('city', models.CharField(help_text='Enter city name', max_length=50, verbose_name='city')),
                ('street', models.CharField(blank=True, help_text='Enter street name', max_length=50, verbose_name='street')),
                ('house', models.CharField(blank=True, max_length=10, verbose_name='house')),
                ('structure', models.CharField(blank=True, max_length=10, verbose_name='structure')),
                ('building', models.CharField(blank=True, max_length=10, verbose_name='building')),
                ('apartment', models.CharField(blank=True, max_length=10, verbose_name='apartment')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter phone number', max_length=128, null=True, region=None, verbose_name='phone')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Personal contacts',
                'db_table': 'contacts',
            },
        ),
    ]
