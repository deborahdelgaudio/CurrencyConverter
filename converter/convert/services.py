# -*- coding: utf-8 -*-
from django.conf import settings

from .models import ConversionRate


def validate_conversion_rates(conversion_params, date=None):
    for currency, rate in conversion_params:
        if not rate:
            if date:
                raise Exception(f"Cannot find conversion rate for {currency} in date {date}")
            raise Exception(f"Cannot find conversion rate for currency: {currency}")


class CurrencyConverter(object):
    """
        CurrencyConverter fetch conversion rate using parameters and convert the amount.
        Has a default currency given by settings.
        Can return all currencies available on database.
    """

    def __init__(self):
        self.default_currency = settings.DEFAULT_CURRENCY

    def get_conversion_rate(self, currency, date=None):
        if currency == self.default_currency:
            return 1
        if date:
            conversion_rate = ConversionRate.objects.filter(date=date, iso_currency=currency).first()
        else:
            conversion_rate = ConversionRate.objects.filter(iso_currency=currency).order_by(
                '-date'
            ).first() # the most recent
        if conversion_rate:
            return conversion_rate.rate
        return None

    def convert(self, src, dest, amount, date=None):
        src_rate = self.get_conversion_rate(src, date)
        dest_rate = self.get_conversion_rate(dest, date)

        validate_conversion_rates([(src, src_rate), (dest, dest_rate)], date)

        if dest != self.default_currency and src != self.default_currency:
            converted_amount = (1 / src_rate) * amount * dest_rate
        elif dest != self.default_currency and src == self.default_currency:
            converted_amount = amount * dest_rate
        elif dest == self.default_currency and src != self.default_currency:
            converted_amount = (1 / src_rate) * amount
        else:
            converted_amount = amount
        return converted_amount

    def get_all_currencies(self):
        currencies = ConversionRate.objects.all().values('iso_currency')
        currencies = list(set([currency['iso_currency'] for currency in currencies]))
        currencies.append(self.default_currency)
        return currencies
