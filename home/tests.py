from django.test import TestCase

from .models import Box


class BoxTestCase(TestCase):
    def setUp(self):
        Box.objects.create(
            name='testBox', logo_url='testLogo.png',
            link_url='http://example.com', sort_order=0)

    def test_box_creation(self):
        """Testing basic box creation"""
        testBox = Box.objects.get(name='testBox')
        self.assertEqual(testBox.name, 'testBox')
        self.assertEqual(testBox.logo_url_static(), 'home/testLogo.png')
