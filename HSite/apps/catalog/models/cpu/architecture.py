from django.db import models
from django.db import IntegrityError


class Architecture(models.Model):
    architecture = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.architecture

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            models.Model.save(self)
        except IntegrityError:
            pass
        finally:
            return Architecture.objects.get(architecture=self.architecture).id
