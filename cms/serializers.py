from rest_framework import serializers

from .models import HeroSection


class HeroSectionModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = HeroSection
        fields = (
            'title',
            'image',
            'short_description',
            'cta_text',
            'link',
        )


class HeroSectionModelSerializerGET(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, attrs):
        return attrs.image.url if attrs.image else ''

    class Meta:
        model = HeroSection
        fields = '__all__'
