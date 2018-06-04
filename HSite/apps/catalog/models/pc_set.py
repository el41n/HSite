from django.db import models, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .cpu.cpu import CPU
from .motherboard.motherboard import Motherboard
from .memory.memory import Memory
from .power_block.power_block import PowerBlock


class PCSet(models.Model):
    class PCSetManager(models.Manager):
        @staticmethod
        def __get_info(Object, id):
            info = None
            info = Object.objects.get(pk=id)
            return info

        @classmethod
        def cpu(cls, id):
            return cls.__get_info(CPU, id)

        @classmethod
        def motherboard(cls, id):
            return cls.__get_info(Motherboard, id)

        @classmethod
        def memory(cls, id):
            return cls.__get_info(Memory, id)

        @classmethod
        def power(cls, id):
            return cls.__get_info(PowerBlock, id)

        def price(self, id):
            return PCSet.objects.cpu()

    class Meta:
        unique_together = ('cpu', 'motherboard', 'memory', 'power')

    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE, default=None, null=True)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE, default=None, null=True)
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, default=None, null=True)
    power = models.ForeignKey(PowerBlock, on_delete=models.CASCADE, default=None, null=True)

    objects = PCSetManager()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            if self.is_valid():
                models.Model.save(self)
                return "Success"
        except IntegrityError:
            return "Already exists"

    def is_valid(self):
        socket_validity = self.cpu.socket_id == self.motherboard.socket_id
        memory_validity = self.motherboard.memory_type_id == self.memory.type_id
        power_validity = self.cpu.power + self.motherboard.power + self.memory.power <= self.power.power_capacity
        return socket_validity and memory_validity and power_validity
