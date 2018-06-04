from django.db import models
from django.db import IntegrityError


class Vendor(models.Model):
    vendor = models.CharField(max_length=25, default='Unknown', unique=True)

    def __str__(self):
        return self.vendor

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            models.Model.save(self)
        except IntegrityError:
            pass
        finally:
            return Vendor.objects.get(vendor=self.vendor).id


class Hardware(models.Model):
    """Super class for all hardware entities"""
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='hardware')
    model = models.CharField(max_length=25, default='Unknown', unique=True)
    _date = models.DateField(auto_now=False, auto_now_add=True, null=True)
    power = models.IntegerField(default=0)
    price = models.IntegerField(default=None, null=True)
    information = models.CharField(max_length=1024, default=None, null=True)

    @property
    def date(self):
        return self._date.year

    def __str__(self):
        return '{} {}'.format(self.vendor, self.model)


