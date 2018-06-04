from django.db import models
from ..motherboard.motherboard import Motherboard
from ..motherboard.socket import Socket
from django.db import IntegrityError
from ..hardware import Hardware
from .architecture import Architecture
from .codename import CodeName


class CPU(Hardware):
    status = models.CharField(max_length=255, default=None, null=True)
    cores = models.IntegerField(default=None, null=True)
    max_clock_speed = models.FloatField(default=None, null=True)
    clock_speed = models.FloatField(default=None, null=True)
    cache = models.FloatField(default=None, null=True)

    socket = models.ForeignKey(Socket, on_delete=models.CASCADE, null=True, related_name='cpu', default=None)

    architecture = models.ForeignKey(Architecture, on_delete=models.CASCADE,
                                     related_name='cpu', null=True, default=None)

    codename = models.ForeignKey(CodeName, on_delete=models.CASCADE, related_name='cpu', null=True,
                                 default=None)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            models.Model.save(self)
        except IntegrityError:
            # old_data = CPU.objects.get(model=self.model)
            # old_data.status = self.status
            # old_data.date = self.date
            # old_data.cores = self.cores
            # old_data.max_clock_speed = self.max_clock_speed
            # old_data.clock_speed = self.clock_speed
            # old_data.cache = self.cache
            # old_data.price = self.price
            # old_data.socket = self.socket
            # old_data.architecture = self.architecture
            # old_data.save()
            pass

