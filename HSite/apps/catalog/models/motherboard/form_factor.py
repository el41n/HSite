from django.db import models
from django.db import IntegrityError


class FormFactor(models.Model):
    form_factor = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.form_factor

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            models.Model.save(self)
        except IntegrityError:
            pass
        finally:
            return FormFactor.objects.get(form_factor=self.form_factor).id
