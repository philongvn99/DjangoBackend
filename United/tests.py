from urllib import response
from django.test import TestCase, SimpleTestCase

# Create your tests here.
class SimpleTest(SimpleTestCase):
    def test_homes_status(self):
        response = self.client.get('/UnitedHome/player/')
        self.assertEquals(response.status_code, 200)