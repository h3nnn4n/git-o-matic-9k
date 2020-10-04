import unittest
from django.test import TestCase, override_settings

import vcr

from github import tasks
from github.models import Developer, Repository


test_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='github/tests/fixtures/vcr_cassettes/'
)


class GetOrUpdateAllUserRepositories(TestCase):
    """
    Tests the add_or_update_all_user_repositories task
    """
    @unittest.skip('Celery config isnt being properly overriden, so the test doesnt work')
    @override_settings(celery_always_eager=True)
    def test_create_all_user_repositories(self):
        """
        Tests that all user repositories are created
        """
        repository_count_before = Repository.objects.count()

        with unittest.mock.patch('celery.celery_always_eager', True, create=True):
            with test_vcr.use_cassette('get_all_repos_from_h3nnn4n.yaml', record='none'):
                tasks.add_or_update_all_user_repositories('h3nnn4n')

        self.assertEqual(repository_count_before + 161, Repository.objects.count())

        repo = Repository.objects.get(name='garapa')
        self.assertEqual(repo.owner_github_id, '')
        self.assertEqual(repo.language, 'C')
        self.assertEqual(repo.full_name, 'h3nnn4n/garapa')


class AddOrUpdateRepositoryTaskTest(TestCase):
    """
    Tests the add_or_update_repository task
    """
    def test_create_repository(self):
        """
        Tests that all user repositories are created
        """
        with test_vcr.use_cassette('get_repo_and_user_h3nnn4n_garapa.yaml', record='none'):
            tasks.add_or_update_repository('h3nnn4n/garapa')

        repository = Repository.objects.first()

        self.assertEqual(repository.full_name, 'h3nnn4n/garapa')


    def test_create_user_for_repository_if_not_found(self):
        """
        Test that if a repository is created without an owner in the database
        it is autmatically created too
        """
        developer_count_before = Developer.objects.count()

        with test_vcr.use_cassette('get_repo_and_user_h3nnn4n_garapa.yaml', record='none'):
            tasks.add_or_update_repository('h3nnn4n/garapa')

        self.assertEqual(developer_count_before + 1, Developer.objects.count())

        dev = Developer.objects.get(login='h3nnn4n')
        self.assertEqual(dev.login, 'h3nnn4n')


    def test_create_repository_found_for_the_first_time(self):
        """
        Test that a repository is created if it is the first time it is found
        """
        repository_count_before = Repository.objects.count()

        with test_vcr.use_cassette('get_repo_and_user_h3nnn4n_garapa.yaml', record='none'):
            tasks.add_or_update_repository('h3nnn4n/garapa')

        self.assertEqual(repository_count_before + 1, Repository.objects.count())

        repo = Repository.objects.get(name='garapa')
        self.assertEqual(repo.name, 'garapa')


    def test_update_existing_repository(self):
        """
        Test that a repository is updated if it was found before
        """
        # Setup
        with test_vcr.use_cassette('get_repo_and_user_h3nnn4n_garapa.yaml', record='none'):
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
    """
    Tests the add_or_update_user task
    """
    def test_create_user(self):
        """
        Test that a user is created with the correct fields
        """
        with test_vcr.use_cassette('get_user_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user('h3nnn4n')

        developer = Developer.objects.get(login='h3nnn4n')

        self.assertEqual(developer.location, 'Brazil')
        self.assertEqual(developer.name, 'Renan S Silva')


    def test_create_user_found_for_the_first_time(self):
        """
        Test that a user is created when it is found for the first time
        """
        developer_count_before = Developer.objects.count()

        with test_vcr.use_cassette('get_user_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user('h3nnn4n')

        self.assertEqual(developer_count_before + 1, Developer.objects.count())


    def test_update_existing_user(self):
        """
        Test that a user is updated if it already exists in the database
        """
        # Setup
        with test_vcr.use_cassette('get_user_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user('h3nnn4n')

        # Lets pretent that the username changed
        dev = Developer.objects.get(login='h3nnn4n')
        dev.login = 'renan'
        dev.save()

        # Actual test
        developer_count_before = Developer.objects.count()

        with test_vcr.use_cassette('get_user_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user('h3nnn4n')

        self.assertEqual(developer_count_before, Developer.objects.count())

        dev = Developer.objects.get(login='h3nnn4n')
        self.assertEqual(dev.login, 'h3nnn4n')


class AddOrUpdateUserFollowersTaskTest(TestCase):
    """
    Tests the add_or_update_user_followers task
    """
    def test_populate_followers(self):
        """
        Test that the followers of an user are properly created and that the
        relation contains the correct data
        """
        with test_vcr.use_cassette('get_user_ruanpablom.yaml', record='none'):
            tasks.add_or_update_user('ruanpablom')

        with test_vcr.use_cassette('get_user_followers_ruanpablom.yaml', record='none'):
            tasks.add_or_update_user_followers('ruanpablom')

        developer = Developer.objects.get(login='ruanpablom')

        self.assertEqual(developer.followers.count(), 10)
        followers_name = [
            follower.login for follower in developer.followers.order_by('login')
        ]

        self.assertEqual(
            sorted(followers_name),
            [
                'GlauberrBatista',
                'Kronossaurus',
                'Mano21',
                'brunats',
                'conejo11',
                'h31nr1ch',
                'lucasaloisio',
                'markx3',
                'rafaelcgs10',
                'wesklei'
            ]
        )

    def test_populate_following_from_followers(self):
        """
        Test that if X is being followed by Y, then Y must also be following X
        """
        with test_vcr.use_cassette('get_user_ruanpablom.yaml', record='none'):
            tasks.add_or_update_user('ruanpablom')

        with test_vcr.use_cassette('get_user_followers_ruanpablom.yaml', record='none'):
            tasks.add_or_update_user_followers('ruanpablom')

        developer_following = Developer.objects.get(login='GlauberrBatista')
        self.assertEqual(developer_following.following.count(), 1)


class AddOrUpdateUserFollowingTaskTest(TestCase):
    """
    Tests the add_or_update_user_followings task
    """
    def test_populate_following(self):
        """
        Test that the users following an user are properly created and that the
        relation contains the correct data
        """
        with test_vcr.use_cassette('get_user_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user('h3nnn4n')

        with test_vcr.use_cassette('get_user_following_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user_followings('h3nnn4n')

        developer = Developer.objects.get(login='h3nnn4n')

        self.assertEqual(developer.following.count(), 4)
        following_names = [
            following.login for following in developer.following.order_by('login')
        ]

        self.assertEqual(
            sorted(following_names),
            ['andrepiske', 'andreynering', 'khskarl', 'rafaelcgs10']
        )

    def test_populate_followers_from_following(self):
        """
        Test that if Y is follows Y, then Y must be followed by X
        """
        with test_vcr.use_cassette('get_user_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user('h3nnn4n')

        with test_vcr.use_cassette('get_user_following_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user_followings('h3nnn4n')

        developer_following = Developer.objects.get(login='andrepiske')
        self.assertEqual(developer_following.followers.count(), 1)


class AddOrUpdateUserStarredRepositoriesTest(TestCase):
    """
    Tests the add_or_update_user_starred_repositories task
    """
    def test_populate_starred_repositories(self):
        """
        Test that the starred repositories of an user are properly created and
        that the relation contains the correct data
        """
        with test_vcr.use_cassette('get_user_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user('h3nnn4n')

        with test_vcr.use_cassette('get_user_stared_repositories_h3nnn4n.yaml', record='none'):
            tasks.add_or_update_user_starred_repositories('h3nnn4n')

        developer = Developer.objects.get(login='h3nnn4n')

        self.assertEqual(developer.starred_repositories.count(), 30)
        starred_repository_names = [
            repository.full_name for repository in developer.starred_repositories.order_by('full_name')
        ]

        self.assertIn('danistefanovic/build-your-own-x', starred_repository_names)


class AddOrUpdateRespositoryStargazersTest(TestCase):
    """
    Tests the add_or_update_repository_stargazers task
    """
    def test_populate_stargazers(self):
        """
        Test that the stargazers of a repository are properly created and that
        the relation contains the correct data
        """
        with test_vcr.use_cassette('get_repo_and_user_h3nnn4n_garapa.yaml', record='none'):
            tasks.add_or_update_repository('h3nnn4n/garapa')

        with test_vcr.use_cassette('get_repo_stargazers_h3nnn4n_garapa.yaml', record='none'):
            tasks.add_or_update_repository_stargazers('h3nnn4n/garapa')

        repository = Repository.objects.get(name='garapa')

        self.assertEqual(repository.stargazers.count(), 12)

        stargazer_names = [
            stargazer.login for stargazer in repository.stargazers.all()
        ]

        self.assertIn('sombreroman55', stargazer_names)
