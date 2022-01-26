import unittest
import os
from urllib.parse import urljoin

import requests

BASE_URL = os.getenv('APP_BASE_URL', 'http://172.17.0.1:9999')

class ClientTest(unittest.TestCase):
    def test_create_root(self):
        slug = 'teacup'
        response = requests.get(urljoin(BASE_URL, f'/{slug}'))
        payload = {'slug': 'teacup', 'text': 'Teacup (tm)'}
        response = requests.post(urljoin(BASE_URL, f'/'), json=payload)
        self.assertEqual(response.status_code, 200)

    def test_create_2nd_root(self):
        slug = 'spork'
        response = requests.get(urljoin(BASE_URL, f'/{slug}'))
        payload = {'slug': 'spork', 'text': 'Sporks'}
        response = requests.post(urljoin(BASE_URL, f'/'), json=payload)
        self.assertEqual(response.status_code, 200)
