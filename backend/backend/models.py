from random import randrange
from django.conf import settings
from django.db import models


class DateMixin(models.Model):
    created_at = models.DateTimeField('Когда создано', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Когда обновлено', auto_now=True, null=True)

    class Meta:
        abstract = True


class InfoMixin(DateMixin):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name='Кем создано',
                                   on_delete=models.SET_NULL,
                                   related_name="+", null=True) 

    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name='Кем обновлено',
                                   on_delete=models.SET_NULL,
                                   related_name="+", null=True)

    class Meta:
        abstract = True

