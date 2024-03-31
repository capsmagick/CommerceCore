from django.contrib import admin
from django.apps import apps


models = apps.get_models()
admin.site.site_header = 'Admin Management'


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        """
            list_display : Fields to be shows to the list of data in the admin site
            search_fields : Fields to be searched on the model
        """

        if model.__name__ == 'User':
            self.list_display = ["username", "first_name", "mobile_number", "is_superuser", "is_customer"]
            self.search_fields = ["username", 'mobile_number', 'first_name']
        else:
            """ Set list_display excluding 'id' fields from foreign keys """
            self.list_display = [field.name for field in model._meta.fields if not field.name.endswith('_id')]

            """ Set search_fields with proper handling of ForeignKey fields """
            self.search_fields = []
            for field in model._meta.fields:
                if not field.name.endswith('_id'):
                    if hasattr(field, 'related_model') and field.related_model:
                        if hasattr(field.related_model, 'name'):
                            self.search_fields.append(f'{field.name}__name')
                    else:
                        self.search_fields.append(field.name)

        super(ListAdminMixin, self).__init__(model, admin_site)


# Register all the model in singe cmd
for model in models:
    model_admin = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, model_admin)
    except admin.sites.AlreadyRegistered:
        pass


