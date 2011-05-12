"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from test_42cc.southtut.models import Knight

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

    def test_models(self):
        self.assertEqual(Knight.objects.count(), 0)
        Knight.objects.create(
            name='First',
            of_the_round_table=True,
            dances_whenever_able=True,
            shrubberies=7,
        )
        self.assertEqual(Knight.objects.count(), 1)
        Knight.objects.all().delete()
        self.assertEqual(Knight.objects.count(), 0)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

