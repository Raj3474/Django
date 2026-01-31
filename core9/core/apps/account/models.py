import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _

from django.db import models

from core.apps.catalogue.models import Product

# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)


        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()




class Customer(AbstractBaseUser, PermissionsMixin):


    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20, blank=True)

    wishlist = models.ManyToManyField(Product, related_name='user_wishlist', blank=True)

    # User status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    objects = CustomAccountManager()

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        print(self.email)
        send_mail(
            subject,
            message,
            '1@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.name


class Address(models.Model):
    """
    Address : Delivery details
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    customer = models.ForeignKey(
        Customer, verbose_name=_("Customer"),
        on_delete=models.CASCADE
    )
    country = CountryField()  # list of all the countries, imported at the top
    full_name = models.CharField(_("Full Name"), max_length=150)
    phone = models.CharField(_("Phone Number"), max_length=50)
    postcode = models.CharField(_("Postcode"),max_length=50)
    address_line1 = models.CharField(_("Address Line 1"),max_length=255)
    address_line2 = models.CharField(_("Address Line 2"),max_length=255)
    town_city = models.CharField(_("Town/City/State"),max_length=150)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("created at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)


    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


    def __str__(self):
        return self.address_line1 + self.address_line2 + self.town_city + self.postcode

