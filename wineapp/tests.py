from django.test import TestCase
from django.utils import timezone

from .models import Wine, Review


class WineTestCase(TestCase):
    def setUp(self):
        ReviewTestCase.setUp(self)

    def test_wine_creation(self):
        """Test basic wine creation"""
        testWine = Wine.objects.get(name='testWine')
        self.assertEqual(testWine.name, 'testWine')


class ReviewTestCase(TestCase):
    def setUp(self):
        Wine.objects.create(name='testWine')
        Review.objects.create(wine=Wine.objects.get(name='testWine'),
            pub_date=timezone.now(), user_name='testUser',
            comment='Meh.', rating=2)

    def test_review_creation(self):
        """Test review attachment to wines"""
        testWine = Wine.objects.get(name='testWine')
        self.assertEqual(testWine.review_set.all().count(), 1)
        testReview = testWine.review_set.get(pk=1)
        self.assertEqual(testReview.comment, 'Meh.')
