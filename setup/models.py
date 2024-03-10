from django.contrib.auth import get_user_model
from django.db import models

# user = get_user_model()


class BaseManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted=False)


class BaseModel(models.Model):
    # created_by = models.ForeignKey('setup.User',
    #                                on_delete=models.SET_NULL,
    #                                null=True, blank=True,
    #                                verbose_name='Created By')
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Created At')

    # updated_by = models.ForeignKey('setup.User',
    #                                on_delete=models.SET_NULL,
    #                                null=True, blank=True,
    #                                verbose_name='Updated By')
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Updated At')

    deleted = models.BooleanField(default=False, verbose_name='Deleted')
    deleted_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Deleted At')
    # deleted_by = models.ForeignKey('setup.User',
    #                                on_delete=models.SET_NULL,
    #                                null=True, blank=True,
    #                                verbose_name='Deleted By')

    objects = BaseManager()

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    class Meta:
        abstract = True
        ordering = ['-updated_at']
