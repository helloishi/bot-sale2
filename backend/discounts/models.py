from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.models import DateMixin

class Discount(DateMixin):
    class Meta:
        verbose_name = _("Скидка")
        verbose_name_plural = _("Скидки")
    
    class PlaceType(models.TextChoices):
        RESTAURANT = "REST", _("Ресторан")
        CAFE = "CAFE", _("Кафе")
        THEATER = "THTR", _("Театр")
        SHOP = "SHOP", _("Магазин")
        OTHER = "OTHR", _("Другое")

    id = models.AutoField(_("ID"), primary_key=True)
    place = models.CharField(_("Место"), max_length=50)

    image = models.ImageField(_("Картинка"), upload_to='images', blank=True)
    description = models.TextField(_("Описание"))
    address_txt = models.CharField(_(""), max_length=100, blank=True)
    start_date = models.DateField(_("Дата начала скидки"), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_("Дата конца скидки"), auto_now=False, auto_now_add=False)
    place_type = models.CharField(_("Тип заведения"), max_length=4, choices=PlaceType.choices, blank=True)

    @property
    def is_active(self):
        return start_date >= datetime.now().date() < end_date

    @property
    def image_link(self):
        return self.image.url

    def __str__(self):
        return f'Скидка в {self.place}'
