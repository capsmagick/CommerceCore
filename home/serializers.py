import datetime
from rest_framework import serializers
from django.conf import settings


def get_first_date_of_month():
    # Function to return the first day of the current month
    today = datetime.datetime.today()
    first_day_of_month = today.replace(day=1)
    return first_day_of_month.date()


def get_last_day_of_month():
    # Function to calculate and return the last day of the current month
    today = datetime.datetime.today()
    first_day_of_next_month = today.replace(month=today.month + 1, day=1)
    last_day_of_current_month = first_day_of_next_month - datetime.timedelta(days=1)
    return last_day_of_current_month.date()


class DashboardSerializer(serializers.Serializer):
    from_date = serializers.DateField(input_formats=settings.DATE_FORMAT, default=get_first_date_of_month)
    to_date = serializers.DateField(input_formats=settings.DATE_FORMAT, default=get_last_day_of_month)

    def validate(self, attrs):
        from_date = attrs.get('from_date')
        to_date = attrs.get('to_date')

        if from_date >= to_date:
            raise serializers.ValidationError({
                'from_date': "Invalid date range: 'from_date' must be before 'to_date'"
            })

        return attrs

    def find_previous_period(self):

        from_date = self.validated_data.get('from_date')
        to_date = self.validated_data.get('to_date')

        period_duration = to_date - from_date

        # Calculate the duration in days of the period
        period_days = period_duration.days if isinstance(period_duration, datetime.timedelta) else period_duration

        # Calculate the current period start and end dates
        current_period_start_date = from_date
        current_period_end_date = current_period_start_date + period_duration - datetime.timedelta(days=1)

        # Check if the provided date range fits within the current period
        if current_period_start_date <= to_date <= current_period_end_date:
            # If the provided range fits in the current period, return the previous period
            previous_period_start_date = current_period_start_date - period_duration
            previous_period_end_date = current_period_end_date - period_duration
        else:
            # If the provided range spans multiple periods, calculate the last complete period before the range
            previous_period_end_date = current_period_start_date - datetime.timedelta(days=1)
            previous_period_start_date = previous_period_end_date - period_duration + datetime.timedelta(days=1)

        return previous_period_start_date, previous_period_end_date

