from datetime import datetime

import pytz

from django.test import TestCase

from github.models import RateLimit


class RateLimitTest(TestCase):
    """
    Tests the RateLimit model
    """
    def test_can_make_new_requests_true(self):
        """
        Check that the record allows news requests if the rate_remaining is high enough
        """
        ratelimit = RateLimit.objects.create(
            rate_limit=15000,
            rate_remaining=8196,
            rate_reset_raw=1601767612,
            rate_reset=datetime(2020, 10, 3, 23, 26, 52, tzinfo=pytz.UTC),
        )

        self.assertTrue(ratelimit.can_make_new_requests())

    def test_can_make_new_requests_false(self):
        """
        Check that the record blocks news requests if the rate_remaining is too low
        """
        ratelimit = RateLimit.objects.create(
            rate_limit=15000,
            rate_remaining=10,
            rate_reset_raw=1601767612,
            rate_reset=datetime(2020, 10, 3, 23, 26, 52, tzinfo=pytz.UTC),
        )

        self.assertFalse(ratelimit.can_make_new_requests())
