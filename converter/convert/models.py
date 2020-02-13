# -*- coding: utf-8 -*-
from django.db import models


class ConversionRate(models.Model):
    iso_currency = models.CharField(max_length=3, unique_for_date='date')
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField()
