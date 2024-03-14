from django.contrib import admin

from .models import Tag
from .models import Attribute
from .models import AttributeGroup
from .models import Brand
from .models import Dimension
from .models import Category

admin.site.register(Tag)
admin.site.register(Attribute)
admin.site.register(AttributeGroup)
admin.site.register(Brand)
admin.site.register(Dimension)
admin.site.register(Category)

