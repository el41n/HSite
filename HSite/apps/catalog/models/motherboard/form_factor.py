from django.db import models


class FormFactor(models.Model):
    form_factor = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.form_factor
