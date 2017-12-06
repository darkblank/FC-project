from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.authtoken.models import Token


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=20,
    )
    # 이메일 인증 전 까지는 is_active = False
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'name',
    ]

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def token(self):
        return Token.objects.get_or_create(user=self)[0].key


class Profile(models.Model):
    USER_TYPE_EMAIL = 'e'
    USER_TYPE_FACEBOOK = 'f'
    CHOICES_USER_TYPE = (
        (USER_TYPE_EMAIL, 'Email'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    nickname = models.CharField(
        max_length=10,
        unique=True,
    )
    user_type = models.CharField(
        max_length=1,
        choices=CHOICES_USER_TYPE,
        default=USER_TYPE_EMAIL,
    )
    profile_image = models.ImageField(
        upload_to='user',
        blank=True,
        null=True,
    )
    preferences = models.ManyToManyField(
        'Preference',
        related_name='preference_set',
        blank=True
    )
    favorites = models.ManyToManyField(
        'restaurants.Restaurant',
        related_name='favorite_set',
        blank=True,
    )
    is_owner = models.BooleanField(
        default=False,
    )
    joined_date = models.DateField(
        auto_now_add=True,
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
