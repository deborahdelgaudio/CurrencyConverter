# -*- coding: utf-8 -*-
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from convert.models import ConversionRate


class ConvertApiTestCase(APITestCase):
    def setUp(self):
        ConversionRate.objects.create(iso_currency='USD', rate='1.0900', date=timezone.now())

    def test_endpoint_without_query_string_params(self):
        """Verify that is possible to call endpoint without passing a query string"""
        url = '/convert/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_conversion_without_a_required_param(self):
        """Verify that is not possible to make conversion without a required parameter"""
        url = '/convert/'
        response = self.client.get(url, {'dest_currency': 'USD', 'amount': '12.4646'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_conversion_with_wrong_date_format(self):
        """Verify that date format accepted is YYY-MM-DD"""
        url = '/convert/'
        response = self.client.get(
            url,
            {
                'src_currency': 'EUR',
                'dest_currency': 'USD',
                'amount': '12.4646',
                'reference_date': '15/02/2020'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_conversion_with_invalid_currency(self):
        """Verify that is not possible to convert an invalid currency"""
        url = '/convert/'
        response = self.client.get(
            url,
            {
                'src_currency': 'ZZZ',
                'dest_currency': 'USD',
                'amount': '12.4646',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_conversion_with_valid_params(self):
        """Verify that is possible to convert amount passing valid parameters"""
        url = '/convert/'
        response = self.client.get(
            url,
            {
                'src_currency': 'EUR',
                'dest_currency': 'USD',
                'amount': '12.4646',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['amount'], f"Missing amount {response.json}")

    def tearDown(self):
        ConversionRate.objects.all().delete()
