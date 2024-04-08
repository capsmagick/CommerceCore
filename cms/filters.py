import django_filters as filters

from .models import HeroSection


class HeroSectionFilter(filters.FilterSet):
    offset = filters.CharFilter(method='generate_view')

    def generate_view(self, queryset, value, *args, **kwargs):
        try:
            offset_value = int(args[0])
            if offset_value:
                queryset = queryset[:offset_value]
        except Exception as e:
            print('Exception occurred at the hero section filter : ', str(e))
        return queryset

    class Meta:
        model = HeroSection
        fields = [
            'cta_text',
            'short_description',
            'link',
        ]


