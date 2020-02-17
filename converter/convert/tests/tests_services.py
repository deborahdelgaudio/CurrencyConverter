# -*- coding: utf-8 -*-
from decimal import *

from django.utils import timezone
from django.test import TestCase

from convert.models import ConversionRate
from convert.services import CurrencyConverter


class CurrencyConverterTest(TestCase):
    def setUp(self):
        self.test_dates = {
            'valid': timezone.now(),
            'invalid': timezone.now() - timezone.timedelta(days=1)
        }
        self.test_currencies = {
            'default': 'EUR',
            'valid': ['GBP', 'USD'],
            'invalid': 'KTR'
        }
        getcontext().prec = 4
        self.test_rate = Decimal('1.0990')
        for currency in self.test_currencies['valid']:
            ConversionRate.objects.create(iso_currency=currency, rate=self.test_rate, date=self.test_dates['valid'])

    def test_get_conversion_rate(self):
        """Verify that conversion rate is available for valid currencies and dates"""
        converter = CurrencyConverter()
        self.assertTrue(
            converter.get_conversion_rate(currency=self.test_currencies['default']),
            f"Default currency {self.test_currencies['default']} has not conversion rate"
        )
        self.assertTrue(
            converter.get_conversion_rate(currency=self.test_currencies['valid'][0]),
            f"A valid currency has not conversion rate: {self.test_currencies['valid'][0]}"
        )
        self.assertFalse(
            converter.get_conversion_rate(currency=self.test_currencies['valid'][0], date=self.test_dates['invalid']),
            f"Conversion rate can be found for an invalid date: {self.test_currencies['valid'][0]}-{self.test_dates['invalid']}"
        )
        self.assertFalse(
            converter.get_conversion_rate(currency=self.test_currencies['invalid']),
            f"Conversion rate can be found for an invalid currency: {self.test_currencies['invalid']}"
        )

    def test_convert(self):
        """Verify the conversion between two currencies"""
        converter = CurrencyConverter()
        test_amount = Decimal('12.3400')

        # EUR - GBP
        src = 'EUR'
        dest = self.test_currencies['valid'][0]

        converted = test_amount * self.test_rate
        converted_by_method = converter.convert(src=src, dest=dest, amount=test_amount, date=self.test_dates['valid'])

        self.assertEqual(
            converted,
            converted_by_method,
            f"Wrong conversion between {src} and {dest}, value: {converted_by_method} expected: {converted}"
        )

        # EUR - EUR
        src = 'EUR'
        dest = 'EUR'

        converted = test_amount
        converted_by_method = converter.convert(src=src, dest=dest, amount=test_amount)

        self.assertEqual(
            converted,
            converted_by_method,
            f"Wrong conversion between {src} and {dest}, value: {converted_by_method} expected: {converted}"
        )

        # GBP - USD
        src = self.test_currencies['valid'][0]
        dest = self.test_currencies['valid'][1]

        converted = test_amount * self.test_rate * (1 / self.test_rate)
        converted_by_method = converter.convert(src=src, dest=dest, amount=test_amount)

        self.assertEqual(
            converted,
            converted_by_method,
            f"Wrong conversion between {src} and {dest}, value: {converted_by_method} expected: {converted}"
        )

    def test_get_all_curriencies(self):
        """Verify that inserted currencies are correctly fetched by converter"""
        converter = CurrencyConverter()
        all_currencies = self.test_currencies['valid']
        all_currencies.append(self.test_currencies['default'])

        self.assertCountEqual(
            all_currencies,
            converter.get_all_currencies(),
            f"Available currencies are not equal to objects currencies: \n{all_currencies}\n{converter.get_all_currencies()}"
        )

    def tearDown(self):
        ConversionRate.objects.all().delete()
