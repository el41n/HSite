from django.db import models
from ..hardware import Hardware
from .memory_type import MemoryType

class Memory(Hardware):
    volume = models.IntegerField(default=None)
    type = models.ForeignKey(MemoryType, on_delete=models.CASCADE, null=True, default=None)
