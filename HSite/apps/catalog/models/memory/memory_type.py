from django.db import models


class MemoryType(models.Model):
    type = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.type
