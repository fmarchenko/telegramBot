__author__ = 'fedor'

from django.db import models


class LastUpdate(models.Model):
    update_id = models.PositiveIntegerField()