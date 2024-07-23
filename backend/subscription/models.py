from datetime import datetime 

from django.utils.translation import gettext_lazy as _
from django.db import models

from backend.models import DateMixin

class Subscription(DateMixin):
    client = models.ForeignKey("user.User", verbose_name=_("Подписчик"), on_delete=models.CASCADE)
    start_date = models.DateField(_("Начало подписки"), auto_now=True, auto_now_add=False)
    end_date = models.DateField(_("Конец подписки"), auto_now=False, auto_now_add=False)
    stopped = models.BooleanField(_("Отменена"), default=False)
    payment_sub_id = models.CharField(_("Идентификатор подписки CloudPayments"), max_length=50)
    
    class Meta:
        verbose_name = _("Подписка")
        verbose_name_plural = _("Подписки")

    @property
    def is_active(self):
        return (self.start_date <= datetime.now().date() < self.end_date) and not self.stopped

    def __str__(self):
        return f"Подписка {self.client.username} до {self.end_date}"
