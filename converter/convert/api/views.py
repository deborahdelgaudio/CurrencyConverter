# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RequestConvertSerializer
from ..models import ConversionRate


def convert_amount(src_rate, dest_rate, amount, src_currency, dest_currency):
    if dest_currency != 'EUR' and src_currency != 'EUR':
        converted_amount = (1 / src_rate) * amount * dest_rate
    elif dest_currency != 'EUR' and src_currency == 'EUR':
        converted_amount = amount * dest_rate
    elif dest_currency == 'EUR' and src_currency != 'EUR':
        converted_amount = (1 / src_rate) * amount
    else:
        converted_amount = amount
    converted_amount = round(converted_amount, 4)
    return converted_amount


@api_view(['GET'])
def get_conversion_api_view(request):
    if request.query_params:
        serializer = RequestConvertSerializer(data=request.query_params)
        if serializer.is_valid():
            dest_currency = serializer.validated_data['dest_currency'].upper()
            src_currency = serializer.validated_data['src_currency'].upper()
            amount = serializer.validated_data['amount']
            date = serializer.validated_data.get('reference_date', None)
            dest_rate = 1
            src_rate = 1

            if dest_currency != 'EUR':
                if date:
                    dest_conversion_rate = ConversionRate.objects.filter(date=date, iso_currency=dest_currency).first()
                else:
                    dest_conversion_rate = ConversionRate.objects.filter(iso_currency=dest_currency).order_by(
                        '-date'
                    ).first()
                if dest_conversion_rate:
                    dest_rate = dest_conversion_rate.rate
                else:
                    return Response(
                        {
                            'message': 'Conversion not available',
                            'errors': serializer.validated_data
                        },
                        status=400
                    )

            if src_currency != 'EUR':
                if date:
                    src_conversion_rate = ConversionRate.objects.filter(date=date, iso_currency=src_currency).first()
                else:
                    src_conversion_rate = ConversionRate.objects.filter(iso_currency=src_currency).order_by(
                        '-date'
                    ).first()
                if src_conversion_rate:
                    src_rate = src_conversion_rate.rate
                else:
                    return Response(
                        {
                            'message': 'Conversion not available',
                            'errors': serializer.validated_data
                        },
                        status=400
                    )

            amount = convert_amount(src_rate, dest_rate, amount, src_currency, dest_currency)
            return Response({'amount': amount, 'currency': dest_currency}, status=200)

        else:
            return Response(
                {
                    'message': 'Bad Request',
                    'errors': serializer.errors
                },
                status=400
            )

    iso_currencies = ConversionRate.objects.all().values('iso_currency')
    currencies = set([currency['iso_currency'] for currency in iso_currencies])

    return Response(
        {
            'message': 'Provide a query string params to convert values',
            'query_parameters': {
                'src_currency': 'currency code of the amount, required',
                'dest_currency': 'currency code of destination, required',
                'amount': 'number with 4 decimal maximum, required',
                'reference_date': 'date YYY-MM-DD, if not specified is the last available on the system'
            },
            'currencies': currencies
        }, status=200
    )
