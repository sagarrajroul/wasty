from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


# Create your models here
class CustomUser(AbstractBaseUser):
    """
    Create and save a User Details.
    """
    username = None
    is_superuser = models.BooleanField(default=False)
    date_joined = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    last_login = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, )
    created_by = models.IntegerField(null=True)
    modified_on = models.DateTimeField(null=True)
    modified_by = models.IntegerField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        db_table = "CUSTOM_USER"
        ordering = ['first_name']

class UserAddress(models.Model):
    profile = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="addresses"
    )
    address = models.TextField(blank=True, default="")
    adhar_number = models.CharField(max_length=20, blank=True, default="")  # Aadhaar
    ddn = models.CharField(max_length=50, blank=True, default="")           # whatever ddn means
    upi_phone = models.CharField(max_length=20, blank=True, default="")
    upi_id = models.CharField(max_length=100, blank=True, default="")
    lane_number = models.CharField(max_length=50, blank=True, default="")
    house_number = models.CharField(max_length=50, blank=True, default="")
    pin_code = models.CharField(max_length=20, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Address {self.pk} for {self.profile}"
