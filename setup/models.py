from django.db import models


class BaseManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = ['-updated_at']
