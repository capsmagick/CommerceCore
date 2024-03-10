from django.db import models
from django.contrib.auth import get_user_model
from .base_model import BaseModel

User = get_user_model()


class AddressRegister(BaseModel):
    ADDRESS_TYPE = (
        ('Billing', 'Billing'),
        ('Shipping', 'Shipping')
    )

    user = models.ForeignKey(User, related_name='useraddress', on_delete=models.SET_NULL, null=True)

    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Full Name')
    contact_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Contact Number')
    alternative_contact_number = models.CharField(max_length=20, blank=True, null=True,
                                                  verbose_name='Alternative Contact Number')

    address_line_1 = models.CharField(max_length=256, blank=True, null=True, verbose_name='House Address')
    address_line_2 = models.CharField(max_length=256, blank=True, null=True, verbose_name='Area Address')
    land_mark = models.CharField(max_length=256, blank=True, null=True, verbose_name='Landmark')

    district = models.CharField(max_length=50, blank=True, null=True, verbose_name='District')
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name='State')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='Country')

    pin_code = models.IntegerField(blank=True, null=True, verbose_name='Pincode')

    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE, blank=True, null=True,
                                    verbose_name='Address Type')

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
