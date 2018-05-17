from django.db import models
from .socket import Socket
from .chipset import Chipset
from ..memory.memory_type import MemoryType
from ..hardware import Hardware
from .form_factor import FormFactor

class Motherboard(Hardware):
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE, related_name='motherboard', null=True)
    chipset = models.ForeignKey(Chipset, on_delete=models.CASCADE, related_name='motherboard', null=True)
    memory_type = models.ForeignKey(MemoryType, on_delete=models.CASCADE, null=True)
    form_factor = models.ForeignKey(FormFactor, on_delete=models.CASCADE, null=True)
