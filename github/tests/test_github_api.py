from datetime import datetime

import pytz

from django.test import TestCase

import vcr

from github.models import RateLimit
from github import github_api


test_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='github/tests/fixtures/vcr_cassettes/'
)


class RateLimitUpdateTest(TestCase):
    """
    Tests the RateLimit auto update feature
    """
    def test_create_rate_limit_object_if_it_doesnt_exit(self):
        """
        Tests that the RateLimit is populated during the first request
        """
        self.assertEqual(RateLimit.objects.count(), 0)

        with test_vcr.use_cassette('ratelimit_get_user_1.yaml', record='none'):
            github_api.get_user('h3nnn4n')

        self.assertEqual(RateLimit.objects.count(), 1)


    def test_update_ratelimit_data(self):
        """
        Tests that the RateLimit is updated with new api calls
        """
        with test_vcr.use_cassette('ratelimit_get_user_1.yaml', record='none'):
            github_api.get_user('h3nnn4n')

        remaining_before = RateLimit.objects.get(pk=1).rate_remaining

        with test_vcr.use_cassette('ratelimit_get_user_2.yaml', record='none'):
            github_api.get_user('h3nnn4n')

        remaining_after = RateLimit.objects.get(pk=1).rate_remaining

        self.assertLess(remaining_after, remaining_before)


class CanMakeNewRequests(TestCase):
    """
    Tests the RateLimit interface
    """
    def test_can_make_new_requests_true_with_no_ratelimit_data(self):
        """
        Check that the record allows one new request if there is not RateLimit
        record on the database. This allows for the rate limit data to be
        fetched.
        """
        self.assertTrue(github_api.can_make_new_requests())

    def test_can_make_new_requests_true(self):
        """
        Check that the record allows news requests if the rate_remaining is high enough
        """
        RateLimit.objects.create(
            id=1,
            rate_limit=5000,
            rate_remaining=42,
            rate_reset_raw=1601767610,
            rate_reset=datetime(2020, 10, 3, 23, 26, 50, tzinfo=pytz.UTC),
        )

        self.assertTrue(github_api.can_make_new_requests())

    def test_can_make_new_requests_false(self):
        """
        Check that the record blocks news requests if the rate_remaining is too low
        """
        RateLimit.objects.create(
            id=1,
            rate_limit=5000,
            rate_remaining=12,
            rate_reset_raw=1601767610,
            rate_reset=datetime(2020, 10, 3, 23, 26, 50, tzinfo=pytz.UTC),
        )

        self.assertFalse(github_api.can_make_new_requests())
