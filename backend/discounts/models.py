from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.models import DateMixin

class Place(DateMixin):
    class PlaceType(models.TextChoices):
        RESTAURANT = "RE", _("Ресторан")
        CAFE = "CA", _("Кафе")
        COFFEE_SHOP = "CF", _("Кофейня")

    id = models.AutoField(_("ID"), primary_key=True)
    name = models.TextField(_("Название"), max_length=60)
    address = models.TextField(_("Адрес"))
    description = models.TextField(_("Описание"))
    place_type = models.CharField(_("Тип заведения"), max_length=2, choices=PlaceType.choices)

    def __str__(self):
        return f"{self.place_type} {self.name}"
    

class Discount(DateMixin):
    id = models.AutoField(_("ID"), primary_key=True)
    place = models.ForeignKey("Place", 
                              verbose_name=_("Заведение"), 
                              on_delete=models.CASCADE)
    description = models.TextField(_("Описание"))
    start_date = models.DateField(_("Дата начала скидки"), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_("Дата конца скидки"), auto_now=False, auto_now_add=False)

    def __str__(self):
        return f'Скидка в {self.place.name}'
