from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.models import DateMixin

class Discount(DateMixin):
    class Meta:
        verbose_name = _("Скидка")
        verbose_name_plural = _("Скидки")
    
    class PlaceType(models.TextChoices):
        RESTAURANT = "RE", _("Ресторан")
        CAFE = "CA", _("Кафе")
        COFFEE_SHOP = "CF", _("Кофейня")

    id = models.AutoField(_("ID"), primary_key=True)
    place = models.CharField(_("Место"), max_length=50)

    description = models.TextField(_("Описание"))
    start_date = models.DateField(_("Дата начала скидки"), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_("Дата конца скидки"), auto_now=False, auto_now_add=False)
    place_type = models.CharField(_("Тип заведения"), max_length=2, choices=PlaceType.choices, blank=True)

    @property
    def is_active(self):
        return start_date >= datetime.now().date() < end_date

    def __str__(self):
        return f'Скидка в {self.place}'
