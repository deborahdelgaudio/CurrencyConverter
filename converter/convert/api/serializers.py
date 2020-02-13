# -*- coding: utf-8 -*-
from rest_framework import serializers


class RequestConvertSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=4, required=True)
    src_currency = serializers.CharField(max_length=3,required=True)
    dest_currency = serializers.CharField(max_length=3, required=True)
    reference_date = serializers.DateField(required=False)