from django.db import models
from django.db import IntegrityError
from ..hardware import Hardware
from .memory_type import MemoryType

class Memory(Hardware):
    volume = models.IntegerField(default=None)
    type = models.ForeignKey(MemoryType, on_delete=models.CASCADE, null=True, default=None)

    def save(self, force_insert=False, force_update=True, using=None,
             update_fields=['volume']):
        try:
            models.Model.save(self)
        except IntegrityError:
            Memory.objects.filter(pf=self.pk).update(price=self.price)
