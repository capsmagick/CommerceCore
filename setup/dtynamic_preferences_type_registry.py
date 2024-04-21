from django import forms
from dynamic_preferences.types import StringPreference
from django.core.validators import URLValidator
from django.core.validators import EmailValidator


class EmailPreference(StringPreference):
    field_class = forms.EmailField

    def validate(self, value):
        super().validate(value)
        EmailValidator()(value)


class URLPreference(StringPreference):
    field_class = forms.URLField

    def validate(self, value):
        super().validate(value)
        URLValidator()(value)

