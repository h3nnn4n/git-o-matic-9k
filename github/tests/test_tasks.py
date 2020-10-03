from django.test import TestCase

import vcr

from github import tasks
from github.models import Developer


test_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='github/tests/fixtures/vcr_cassettes/'
)


class AddOrUpdateUserTaskTest(TestCase):
    def test_potato(self):
        developer_count_before = Developer.objects.count()

        with test_vcr.use_cassette('get_user_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user('h3nnn4n')

        self.assertEqual(developer_count_before + 1, Developer.objects.count())
