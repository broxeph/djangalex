from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test.client import Client
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import Wine, Review


def setUpModule():
    print('Module setup...')


def tearDownModule():
    print('Module teardown...')


class UrlTestCase(TestCase):
    def test_homepage_connection(self):
        response = self.client.get(reverse('wineapp:index'))
        self.assertEqual(response.status_code, 200)

    def test_recommendations_connection(self):
        response = self.client.get(reverse('wineapp:index'))
        self.assertEqual(response.status_code, 200)


class WineTestCase(TestCase):
    def setUp(self):
        ReviewTestCase.setUp(self)

    def test_wine_creation(self):
        """Test basic wine creation"""
        testWine = Wine.objects.get(name='testWine')
        self.assertEqual(testWine.name, 'testWine')


class ReviewTestCase(TestCase):
    def setUp(self):
        testUser = User.objects.create_user(
            username='testUser', email='test@example.com', password='hunter2')
        Wine.objects.create(name='testWine')
        Review.objects.create(
            wine=Wine.objects.get(name='testWine'),
            pub_date=timezone.now(), user_name=testUser.username,
            comment='Meh.', rating=2)

    def test_review_creation(self):
        """Test review attachment to wines"""
        testWine = Wine.objects.get(name='testWine')
        self.assertEqual(testWine.review_set.all().count(), 1)
        testReview = testWine.review_set.get(pk=1)
        self.assertEqual(testReview.comment, 'Meh.')


class UserTestCase(TestCase):
    def setUp(self):
        ReviewTestCase.setUp(self)
        setup_test_environment()
        self.client = Client()

    def test_user_creation(self):
        """Test basic user creation"""
        testUser = User.objects.get(username='testUser')
        self.assertEqual(testUser.username, 'testUser')

    def test_recommendations(self):
        """Test user recommendations for anonymous user"""
        response = self.client.get(reverse('wineapp:user_recommendation_list'))
        self.assertEqual(response.status_code, 302)

        """Test user recommendations for logged-in user"""
        testWineTwo = Wine.objects.create(name='testWineTwo')
        self.logged_in = self.client.login(
            username='testUser', password='hunter2')
        self.assertTrue(self.logged_in)
