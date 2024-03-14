import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
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

    store_manager = models.BooleanField(default=False)

    ########################################
    # BaseModel
    ########################################
    created_by = models.ForeignKey('User', related_name='%(class)s_created_by',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Created By')
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Created At')

    updated_by = models.ForeignKey('User', related_name='%(class)s_updated_by',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Updated By')
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Updated At')

    deleted = models.BooleanField(default=False, verbose_name='Deleted')
    deleted_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Deleted At')
    deleted_by = models.ForeignKey('User', related_name='%(class)s_deleted_by',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Deleted By')

    ########################################

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
