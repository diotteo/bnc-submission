import unittest
import os
from urllib.parse import urljoin

import requests

BASE_URL = os.getenv('APP_BASE_URL', 'http://172.17.0.1:9999')

class ClientTest(unittest.TestCase):
    """For the tests to pass, make sure BASE_URL is set correctly (or export APP_BASE_URL from the environment) and delete (or move) the app.db database (run.sh will recreate it)"""
    def test_create_root(self):
        slug = 'teacup'
        response = requests.get('/'.join((BASE_URL, f'{slug}')))
        payload = {'slug': 'teacup', 'text': 'Teacup (tm)'}
        response = requests.post('/'.join((BASE_URL, '')), json=payload)
        self.assertEqual(response.status_code, 200)

    def test_create_2nd_root(self):
        slug = 'spork'
        response = requests.get('/'.join((BASE_URL, f'{slug}')))
        payload = {'slug': 'spork', 'text': 'Sporks'}
        response = requests.post('/'.join((BASE_URL, '')), json=payload)
        self.assertEqual(response.status_code, 200)

    def test_create_tree(self):
        paths = ['spork/fork', 'spork/fork/spoon', 'spork/spoon', 'spork/fork/fork', 'spork/fork/fork/knife']
        for full_path in paths:
            path, slug = full_path.rsplit('/', maxsplit=1)
            payload = {'slug': slug, 'text': slug.capitalize()}
            response = requests.post('/'.join((BASE_URL, path)), json=payload)
            self.assertEqual(response.status_code, 200)
            print(response.json())

    def test_update_far_child(self):
        full_path = 'spork/fork/fork/knife'
        path, slug = full_path.rsplit('/', maxsplit=1)
        payload = {'slug': slug, 'text': slug.capitalize() + '2'}
        response = requests.post('/'.join((BASE_URL, path)), json=payload)
        self.assertEqual(response.status_code, 200)
        print(response.json())
