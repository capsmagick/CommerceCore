import django_filters as filters

from users.models import AddressRegister


class AddressRegisterFilter(filters.Filter):
    class Meta:
        model = AddressRegister
        fields = ['user']


