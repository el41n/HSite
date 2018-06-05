from django.db import models, IntegrityError
from ..hardware import Hardware


class PowerBlock(Hardware):
    power_capacity = models.IntegerField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            models.Model.save(self)
        except IntegrityError:
            PowerBlock.objects.filter(pf=self.pk).update(price=self.price)
