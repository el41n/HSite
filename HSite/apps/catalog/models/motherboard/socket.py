from django.db import models
from django.db import IntegrityError


class Socket(models.Model):
    socket = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.socket

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            models.Model.save(self)
        except IntegrityError:
            pass
        finally:
            return Socket.objects.get(socket=self.socket).id
