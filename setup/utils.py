from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def generate_field_name(field):
    name = field.name

    if name.find('_') == -1:
        return name.capitalize()
    else:
        split_name = name.split('_')
        new_name = ' '.join(word.title() for word in split_name)
        return new_name


def generate_column(model, actions=True, default_fields=None):
    """
        Function to create list of fields in any table
    """

    fields = model._meta.fields

    columns = []

    for dbfield in fields:
        if dbfield.name in default_fields:
            columns.append({
                "value": dbfield.name,
                "text": dbfield.verbose_name if dbfield.verbose_name else generate_field_name(dbfield),
                "is_default": True
            })

        else:
            columns.append({
                "value": dbfield.name,
                "text": dbfield.verbose_name if dbfield.verbose_name else generate_field_name(dbfield),
                "is_default": False
            })

    if actions:
        columns.append({
            "value": 'actions',
            "text": 'Actions',
            "is_default": True
        })

    return columns


def compress_image(pic):
    """
        Function to compress the image to make thumb nile image
    """
    im = Image.open(pic)
    if im.mode == 'RGBA':
        im = im.convert('RGB')

    # Perform compression operations here
    image_io = BytesIO()
    im.save(image_io, format='JPEG', quality=40)  # Adjust quality as needed
    content_file = ContentFile(image_io.getvalue())

    return content_file


