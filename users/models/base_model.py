from django.db import models

from users.models import User


class BaseManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted=False)


class BaseModel(models.Model):
    created_by = models.ForeignKey(User, related_name='%(class)s_created_by',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Created By')
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Created At')

    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Updated By')
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Updated At')

    deleted = models.BooleanField(default=False, verbose_name='Deleted')
    deleted_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Deleted At')
    deleted_by = models.ForeignKey(User, related_name='%(class)s_deleted_by',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Deleted By')

    objects = BaseManager()

    def delete(self, *args, **kwargs):
        from setup.middleware.request import CurrentRequestMiddleware
        user = CurrentRequestMiddleware.get_request().user

        self.deleted = True
        self.deleted_by = user
        self.save()

    def save(self, *args, **kwargs):
        from setup.middleware.request import CurrentRequestMiddleware
        user = CurrentRequestMiddleware.get_request().user
        if self.id is None:
            self.created_by = user
            self.updated_by = user
        else:
            if user.is_authenticated:
                self.updated_by = user
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['-updated_at']
