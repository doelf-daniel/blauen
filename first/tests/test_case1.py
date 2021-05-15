from django.test import TestCase


class ThingTestCase(TestCase):

    def test_query_empty_db(self):
        self.assertTrue(True)
