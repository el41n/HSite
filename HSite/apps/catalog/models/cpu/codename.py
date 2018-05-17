from django.db import models


class CodeName(models.Model):
    codename = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.codename
