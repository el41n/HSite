from django.db import models


class Vendor(models.Model):
    vendor = models.CharField(max_length=25, default='Unknown', unique=True)

    def __str__(self):
        return self.vendor


class Hardware(models.Model):
    """Super class for all hardware entities"""
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='hardware')
    model = models.CharField(max_length=25, default='Unknown', unique=True)
    _date = models.DateField(auto_now=False, auto_now_add=False)
    power = models.IntegerField(default=0)
    price = models.IntegerField(default=None, null=True)
    information = models.CharField(max_length=1024, default=None)

    @property
    def date(self):
        return self._date.year

    def __str__(self):
        return '{} {}'.format(self.vendor, self.model)


