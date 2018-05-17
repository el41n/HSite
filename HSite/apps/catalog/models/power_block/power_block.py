from django.db import models
from ..hardware import Hardware


class PowerBlock(Hardware):
    power_capacity = models.IntegerField()
