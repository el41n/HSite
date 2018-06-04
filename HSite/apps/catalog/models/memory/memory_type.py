from django.db import models
from django.db import IntegrityError


class MemoryType(models.Model):
    type = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.type

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            models.Model.save(self)
        except IntegrityError:
            pass
        finally:
            return MemoryType.objects.get(type=self.type).id
