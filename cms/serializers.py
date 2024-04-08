from rest_framework import serializers

from .models import HeroSection


class HeroSectionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = HeroSection
        fields = (
            'image',
            'short_description',
            'cta_text',
            'link',
        )


class HeroSectionModelSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = '__all__'
