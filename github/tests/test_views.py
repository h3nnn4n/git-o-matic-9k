from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

import vcr

from github.tasks import add_or_update_repository


test_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='github/tests/fixtures/vcr_cassettes/'
)


def populate_records():
    with test_vcr.use_cassette('get_many_repo_and_users.yaml', record='none'):
        add_or_update_repository('89netraM/MazeGenerator')
        add_or_update_repository('Droogans/unmaintainable-code')
        add_or_update_repository('LukasLoeffler/pgtools')
        add_or_update_repository('MechanicalSoup/MechanicalSoup')
        add_or_update_repository('NVlabs/imaginaire')
        add_or_update_repository('andrepiske/wowhttp')
        add_or_update_repository('czytcn/WindowsNT6QuickSet')
        add_or_update_repository('dendronhq/dendron')
        add_or_update_repository('felipefialho/awesome-made-by-brazilians')
        add_or_update_repository('h3nnn4n/Mandelbrot-Explorer')
        add_or_update_repository('h3nnn4n/garapa')
        add_or_update_repository('h3nnn4n/png2gb')
        add_or_update_repository('h3nnn4n/smart-panda')
        add_or_update_repository('mozilla/FirefoxColor')
        add_or_update_repository('scrapy/itemadapter')
        add_or_update_repository('sharkdp/bat')


class RepositoryViewSetTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser')
        client = APIClient()
        client.force_authenticate(user=user)

        populate_records()
        self.api_client = client

    def test_has_next(self):
        response = self.api_client.get(reverse('repository-list'))
        self.assertIsNotNone(response.json()['next'])

        response = self.api_client.get(response.json()['next'])
        self.assertIsNone(response.json()['next'])

    def test_filter_language_is_c(self):
        response = self.api_client.get(reverse('repository-list'), {'language': 'C'})
        self.assertEqual(len(response.json()['results']), 2)

    def test_filter_language_is_rust(self):
        response = self.api_client.get(reverse('repository-list'), {'language': 'Rust'})
        self.assertEqual(len(response.json()['results']), 4)

    def test_filter_homepage_isnull_true(self):
        response = self.api_client.get(reverse('repository-list'), {'homepage__isnull': True})
        self.assertEqual(len(response.json()['results']), 2)

    def test_filter_homepage_isnull_false(self):
        response = self.api_client.get(reverse('repository-list'), {'homepage__isnull': False})
        self.assertEqual(len(response.json()['results']), 10)

    def test_filter_stargazers_count_lte_50(self):
        response = self.api_client.get(reverse('repository-list'), {'stargazers_count__lte': 50})
        self.assertEqual(len(response.json()['results']), 9)

    def test_filter_stargazers_count_gte_50(self):
        response = self.api_client.get(reverse('repository-list'), {'stargazers_count__gte': 50})
        self.assertEqual(len(response.json()['results']), 8)


class DeveloperViewSetTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser')
        client = APIClient()
        client.force_authenticate(user=user)

        populate_records()
        self.api_client = client

    def test_has_next(self):
        response = self.api_client.get(reverse('developer-list'))
        self.assertIsNotNone(response.json()['next'])

        response = self.api_client.get(response.json()['next'])
        self.assertIsNone(response.json()['next'])

    def test_filter_name_isnull(self):
        response = self.api_client.get(reverse('developer-list'), {'name__isnull': True})
        self.assertEqual(len(response.json()['results']), 2)

    def test_filter_locations_is_brazil(self):
        response = self.api_client.get(reverse('developer-list'), {'location': 'Brazil'})
        self.assertEqual(len(response.json()['results']), 1)
