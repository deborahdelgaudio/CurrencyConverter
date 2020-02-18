# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone

from convert.models import ConversionRate


class Command(BaseCommand):
    help = 'Download xml file with the last 90 days exchange rates and update the database'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, help='Url of xml file with the last 90 days exchange rates')
        parser.add_argument('-c', '--clean', type=int, help='Remove from database rates older than X days')

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        clean_days = kwargs['clean']

        if url:
            res = requests.get(url)
            if res.status_code == 200:
                parsed = minidom.parseString(res.text).toprettyxml(indent="  ")
                with open(settings.RATES_PATH, 'w') as file:
                    file.write(parsed)

        tree = ET.parse(settings.RATES_PATH)
        root = tree.getroot()
        for child in root[2]:
            date = str(child.get('time'))
            for rate in child:
                currency = str(rate.get('currency'))
                rate_value = float(rate.get('rate'))
                try:
                    ConversionRate.objects.filter(date=date, iso_currency=currency).get()
                except models.ObjectDoesNotExist:
                    obj = ConversionRate(date=date, iso_currency=currency, rate=rate_value)
                    obj.save()
                    self.stdout.write(
                        self.style.SUCCESS('ConversionRate "%s (%s)" created with success!' % (obj.iso_currency, obj.date))
                    )

        if clean_days:
            deadline = timezone.datetime.today() - timezone.timedelta(days=clean_days)
            ConversionRate.objects.filter(date__lt=deadline).delete()
