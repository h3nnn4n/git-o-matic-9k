from django.test import TestCase

import vcr

from github import tasks
from github.models import Developer, Repository


test_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='github/tests/fixtures/vcr_cassettes/'
)


class AddOrUpdateRepositoryTaskTest(TestCase):
    def test_create_repository_found_for_the_first_time(self):
        repository_count_before = Repository.objects.count()

        with test_vcr.use_cassette('get_repo_h3nnn4n_garapa.yaml', record='none'):
            tasks.add_or_update_repository('h3nnn4n/garapa')

        self.assertEqual(repository_count_before + 1, Repository.objects.count())

        repo = Repository.objects.get(name='garapa')
        self.assertEqual(repo.name, 'garapa')


    def test_update_existing_repository(self):
        # Setup
        with test_vcr.use_cassette('get_repo_h3nnn4n_garapa.yaml', record='none'):
            tasks.add_or_update_repository('h3nnn4n/garapa')

        # Lets pretent that the description changed
        repo = Repository.objects.get(name='garapa')
        repo.description = ''
        repo.save()

        # Actual test
        repository_count_before = Repository.objects.count()

        with test_vcr.use_cassette('get_repo_h3nnn4n_garapa.yaml', record='none'):
            tasks.add_or_update_repository('h3nnn4n/garapa')

        self.assertEqual(repository_count_before, Repository.objects.count())

        dev = Repository.objects.get(name='garapa')
        self.assertEqual(dev.description,
            'A gameboy emulator, written in C with an optional tetris AI and Julia API'
        )


class AddOrUpdateUserTaskTest(TestCase):
    def test_create_user_found_for_the_first_time(self):
        developer_count_before = Developer.objects.count()

        with test_vcr.use_cassette('get_user_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user('h3nnn4n')

        self.assertEqual(developer_count_before + 1, Developer.objects.count())


    def test_update_existing_user(self):
        # Setup
        with test_vcr.use_cassette('get_user_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user('h3nnn4n')

        # Lets pretent that the username changed
        dev = Developer.objects.get(user_name='h3nnn4n')
        dev.user_name = 'renan'
        dev.save()

        # Actual test
        developer_count_before = Developer.objects.count()

        with test_vcr.use_cassette('get_user_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user('h3nnn4n')

        self.assertEqual(developer_count_before, Developer.objects.count())

        dev = Developer.objects.get(user_name='h3nnn4n')
        self.assertEqual(dev.user_name, 'h3nnn4n')
