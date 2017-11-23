from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('올바른 주소를 입력해주세요.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class ExtraUserInfo(models.Model):
    USER_TYPE_CUSTOMER = 'c'
    USER_TYPE_FACEBOOK = 'f'
    CHOICES_USER_TYPE = (
        (USER_TYPE_CUSTOMER, 'Customer'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
    )
    user_type = models.CharField(
        max_length=1,
        choices=CHOICES_USER_TYPE,
        default=USER_TYPE_CUSTOMER,
    )
    nickname = models.CharField(
        max_length=10,
        unique=True,
    )
    phone_number = models.CharField(
        max_length=13,
    )
    profile_image = models.ImageField(
        upload_to='user',
        blank=True,
        null=True,
    )
    is_owner = models.BooleanField(
        default=False,
    )
    joined_date = models.DateField(
        auto_now_add=True,
    )
    preferences = models.ManyToManyField(
        'Preference',
    )
    favorites = models.ManyToManyField(
        'restaurants.Restaurant',
    )


class Preference(models.Model):
    CHOICES_FOOD_TYPE = (
        ('kor', 'Korean'),
        ('chn', 'Chinese'),
        ('jpn', 'Japanese'),
        ('mex', 'Mexican'),
        ('amc', 'American'),
        ('tha', 'Thai'),
        ('med', 'Mediterranean'),
        ('ita', 'Italian'),
        ('vtn', 'Vietnamese'),
        ('spn', 'Spanish'),
        ('ind', 'Indian'),
        ('etc', 'Etc'),
    )
    preferences = models.CharField(
        max_length=3,
        choices=CHOICES_FOOD_TYPE,
        blank=True,
    )
