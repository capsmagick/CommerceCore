from django.db import models
from users.models.base_model import BaseModel


class HeroSection(BaseModel):
    cta_text = models.CharField(max_length=256, verbose_name='CTA Button Text')
    short_description = models.CharField(max_length=256, verbose_name='Short Description')
    link = models.CharField(max_length=512, verbose_name='CTA Button Link')
    image = models.ImageField(upload_to='hero/images', verbose_name='Image')

