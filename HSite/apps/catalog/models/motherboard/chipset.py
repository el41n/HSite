from django.db import models


class Chipset(models.Model):
    # class Meta:
    #     unique_together = ('vendor', 'model')

    #vendor = models.CharField(max_length=25)
    chipset = models.CharField(max_length=255)

    def __str__(self):
        return self.chipset
