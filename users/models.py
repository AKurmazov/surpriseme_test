from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, second_name, password=None):
        if not email:
            raise ValueError("Users must have an email")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not second_name:
            raise ValueError("Users must have a second name")

        user = self.model(
            email=email,
            first_name=first_name,
            second_name=second_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, second_name, password):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            second_name=second_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", blank=False, unique=True)
    phone = PhoneNumberField(verbose_name="phone", null=True, blank=True)
    first_name = models.CharField(verbose_name="first name", max_length=40, blank=False)
    second_name = models.CharField(verbose_name="second name", max_length=40, blank=False)
    revenue = models.FloatField(verbose_name="revenue", default=0)

    # default fields
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'second_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return f"{self.first_name} {self.second_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
