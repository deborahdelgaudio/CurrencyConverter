# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RequestConvertSerializer
from ..services import CurrencyConverter


@api_view(['GET'])
def get_conversion_api_view(request):
    """
        Convert amount from src_currency to dest_currency, using a conversion rate referenced at reference_date
    """
    converter = CurrencyConverter()

    if request.query_params:

        serializer = RequestConvertSerializer(data=request.query_params)

        if serializer.is_valid():

            dest_currency = serializer.validated_data['dest_currency'].upper()
            src_currency = serializer.validated_data['src_currency'].upper()
            amount = serializer.validated_data['amount']
            date = serializer.validated_data.get('reference_date', None)

            try:
                converted_amount = converter.convert(src=src_currency, dest=dest_currency, amount=amount, date=date)
            except Exception as e:
                return Response(
                    {
                        'message': e.args[0],
                        'errors': serializer.validated_data
                    },
                    status=400
                )

            converted_amount = round(converted_amount, 4)  # represent converted amount with max 4 decimal
            return Response(
                {
                    'amount': converted_amount,
                    'currency': dest_currency
                },
                status=200
            )

        else:
            return Response(
                {
                    'message': 'Bad Request',
                    'errors': serializer.errors
                },
                status=400
            )

    return Response(
        {
            'message': 'Provide a query string to convert values',
            'query_parameters': {
                'src_currency': 'currency code of the amount, required',
                'dest_currency': 'currency code of destination, required',
                'amount': 'number with 4 decimal maximum, required',
                'reference_date': 'date YYY-MM-DD, if not specified is the last available on the system'
            },
            'currencies': converter.get_all_currencies()
        }, status=200
    )
