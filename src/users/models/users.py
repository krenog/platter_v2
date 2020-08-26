from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


# Create your models here.


class UserType(models.Model):
    type_name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'тип пользователя'
        verbose_name_plural = 'Типы пользователей'

    def __str__(self):
        return self.type_name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number: str, password: str, **extra_fields) -> 'User':
        """
        Create and save a user with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError('phone_number must be set')
        if not phone_number.isnumeric():
            raise ValueError('phone_number must be numeric')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.is_superuser = False
        user.is_active = True
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields) -> 'User':
        return self._create_user(phone_number, password, **extra_fields)

    def get_or_create_user(self, phone_number: str, **extra_fields) -> 'User':
        try:
            user = self.get(phone_number=phone_number)
        except self.model.DoesNotExist:
            user = self.create_user(phone_number, **extra_fields)

        return user

    def create_staffuser(self, phone_number, password):
        user = self.create_user(
            phone_number,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(
            phone_number,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    Unknown = 0
    Male = 1
    Female = 2
    SEX_CHOICES = (
        (Unknown, 'Unknown'),
        (Male, 'Male'),
        (Female, 'Female'),
    )
    USER = 0
    ADMIN = 1
    USER_TYPES = (
        (USER, 'User'),
        (ADMIN, 'Admin'),
    )

    objects = UserManager()
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True,
                                        verbose_name="Запись создана")
    phone_number = models.CharField(max_length=10, unique=True)
    user_type = models.IntegerField(choices=USER_TYPES, null=False, blank=False, default=USER,
                                    verbose_name="Электронная почта")
    email = models.EmailField(null=True, blank=True, verbose_name="Электронная почта")
    sex = models.IntegerField(choices=SEX_CHOICES, null=False, blank=False, default=Unknown)
    birth = models.DateField(null=True, blank=True,
                             verbose_name="Дата рождения")
    first_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Имя')
    last_name = models.CharField(max_length=150, null=False, blank=False, verbose_name='Фамилия')

    USERNAME_FIELD = 'phone_number'
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.phone_number)


class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # пользователь
    refresh_token = models.CharField(max_length=500, null=True, verbose_name='Пуш токе')
    device_id = models.CharField(max_length=256, verbose_name='Ид устройства')
    push_token = models.CharField(max_length=500, null=True)

    class Meta:
        verbose_name = 'устройство'
        verbose_name_plural = 'Устройства'

    def __str__(self):
        return str(self.device_id)
