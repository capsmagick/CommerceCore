import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from setup.models import BaseModel

from rest_framework_simplejwt.tokens import RefreshToken


def generate_customer_id():
    now = datetime.datetime.now()
    return "".join(now.strftime("%Y%b%d%H%M%S%f"))


class User(AbstractUser):
    GENDER = (
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Prefer Not to say', 'Prefer Not to say'),
    )

    is_customer = models.BooleanField(default=False)
    customer_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='Customer ID')
    mobile_number = models.CharField(null=True, max_length=15, verbose_name='Mobile Number')

    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Date Of Birth')
    gender = models.CharField(choices=GENDER, max_length=25, blank=True, null=True, verbose_name='Gender')

    profile_picture = models.FileField(upload_to='profile/', blank=True, null=True, verbose_name='Profile Picture')

    is_suspended = models.BooleanField(default=False)

    # created_by = models.ForeignKey('setup.User',
    #                                on_delete=models.SET_NULL,
    #                                null=True, blank=True, related_name='user_createdby',
    #                                verbose_name='Created By')
    # created_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Created At')
    #
    # updated_by = models.ForeignKey('setup.User',
    #                                on_delete=models.SET_NULL,
    #                                null=True, blank=True, related_name='user_updatedby',
    #                                verbose_name='Updated By')
    # updated_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Updated At')
    #
    # deleted = models.BooleanField(default=False, verbose_name='Deleted')
    # deleted_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Deleted At')
    # deleted_by = models.ForeignKey('setup.User',
    #                                on_delete=models.SET_NULL,
    #                                null=True, blank=True, related_name='user_deletedby',
    #                                verbose_name='Deleted By')

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.get_full_name() if self.first_name else self.username

    def save(self, *args, **kwargs):
        if self.is_customer and not self.customer_id:
            self.customer_id = generate_customer_id()
        super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


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
                                    verbose_name='Full Name')

    is_default = models.BooleanField(default=False)
