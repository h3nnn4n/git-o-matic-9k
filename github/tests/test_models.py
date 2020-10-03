from datetime import datetime

import pytz

from django.test import TestCase

from github.models import RateLimit


class RateLimitTest(TestCase):
    def test_can_make_new_requests_true(self):
        ratelimit = RateLimit.objects.create(
            rate_limit=5000,
            rate_remaining=256,
            rate_reset_raw=1601767610,
            rate_reset=datetime(2020, 10, 3, 23, 26, 50, tzinfo=pytz.UTC),
        )

        self.assertTrue(ratelimit.can_make_new_requests())

    def test_can_make_new_requests_false(self):
        ratelimit = RateLimit.objects.create(
            rate_limit=5000,
            rate_remaining=42,
            rate_reset_raw=1601767610,
            rate_reset=datetime(2020, 10, 3, 23, 26, 50, tzinfo=pytz.UTC),
        )

        self.assertFalse(ratelimit.can_make_new_requests())
