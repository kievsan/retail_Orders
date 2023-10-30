from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

USER_TYPE_CHOICES = (
    ('shop', _('Shop')),
    ('buyer', _('Buyer')),
)

CONTACT_ITEMS_LIMIT = 5


class UserManager(BaseUserManager):
    """
    Миксин для управления пользователями
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The email must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Swapped user model
    """
    REQUIRED_FIELDS = ['last_name', 'first_name', 'patronymic', 'type', 'company', 'position']
    USERNAME_FIELD = 'email'
    MAIL_FIELD = "email"
    RELATED_DB = 'contacts'
    objects = UserManager()
    current_validator = UnicodeUsernameValidator()

    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    patronymic = models.CharField(_('patronymic'), max_length=30, blank=True)
    company = models.CharField(_('company'), help_text=_('Enter company name'), max_length=50, blank=True)
    position = models.CharField(_('position'), help_text=_('Enter staff position in company'), max_length=50, blank=True)
    type = models.CharField(_('user type'), choices=USER_TYPE_CHOICES, max_length=10, default='buyer')

    username = models.CharField(_('user name'), max_length=10, unique=False, blank=True)
    # username = None
    ''' ?????!
        username = None
        -------------------------
        $ python manage.py makemigrations
        
        SystemCheckError: System check identified some issues:
        ERRORS:
        <class 'api_auth.admin.CustomUserAdmin'>: (admin.E033) The value of 'ordering[0]' refers to 'username', 
        which is not a field of 'api_auth.User'.
    '''
    email = models.EmailField(
        _('email address'),
        max_length=50,
        help_text=_('Enter email address. Letters, digits and @/./+/-/_ only.'),
        validators=[current_validator],
        error_messages={
            'unique': _("A user with that email already exists."),
        },
        unique=True,
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    def __str__(self):
        return f'{self.email}: {self.first_name} {self.last_name}'

    class Meta(AbstractUser.Meta):
        db_table = 'users'
        ordering = ('email',)


class Contact(models.Model):
    """
    User contacts model.
        At least one of the following fields is required:
        :param str person: contact name;
        :param PhoneNumber phone: contact phone;
        :param str city, street, house, structure, building, apartment : contact address.
    """
    to_user = models.ForeignKey(User, verbose_name=_('user'), related_name=User.RELATED_DB, on_delete=models.CASCADE)
    person = models.CharField(_('contact person'), help_text=_('Enter contact person'), max_length=50, blank=True)
    city = models.CharField(_('city'), help_text=_('Enter city name'), max_length=50, null=False, blank=False)
    street = models.CharField(_('street'), help_text=_('Enter street name'), max_length=50, blank=True)
    house = models.CharField(_('house'), max_length=10, blank=True)
    structure = models.CharField(_('structure'), max_length=10, blank=True)
    building = models.CharField(_('building'), max_length=10, blank=True)
    apartment = models.CharField(_('apartment'), max_length=10, blank=True)
    phone = PhoneNumberField(_('phone'), help_text=_('Enter phone number'), null=True, blank=True)

    def save(self, *args, **kwargs):
        contacts = Contact.objects.filter(to_user_id=self.to_user.id)
        # if contacts.count() < CONTACT_ITEMS_LIMIT or contacts.filter(id=self.id).exists():
        #     super(Contact, self).save(*args, **kwargs)
        if contacts.count() < CONTACT_ITEMS_LIMIT:
            super(Contact, self).save(*args, **kwargs)
        else:
            raise ValidationError(f'There are already {CONTACT_ITEMS_LIMIT} contacts. No more!')

    def __str__(self):
        return f'{self.person}, {self.phone}, {self.city} {self.street} {self.house}'

    class Meta:
        db_table = User.RELATED_DB
        verbose_name = _('Contact')
        verbose_name_plural = _('Personal contacts')
