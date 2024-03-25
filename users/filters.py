import django_filters as filters

from users.models import AddressRegister


class AddressRegisterFilter(filters.FilterSet):
    class Meta:
        model = AddressRegister
        fields = ['user']


