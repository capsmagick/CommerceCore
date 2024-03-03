
def generate_field_name(field):
    name = field.name

    if name.find('_') == -1:
        return name.capitalize()
    else:
        split_name = name.split('_')
        new_name = ' '.join(word.title() for word in split_name)
        return new_name


def generate_column(model, actions=True, default_fields=None):
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


