from django.test import TestCase
from django.urls import reverse
from . import utils

class TestView(TestCase):
    """
    Test that access to views that accept get do not raise exception.
    """
    def setUp(self) -> None:
        self.views = [
            {"name": 'index', 'requires_authentication': False},
            {"name": 'about', 'requires_authentication': False},
        ]
        self.configuration = utils.createConfiguration()
        return super().setUp()

    def test_access_to_views(self):
        for view in self.views:
            view_name = view['name']
            response = self.client.get(reverse(f'core:{view_name}'))
            if view['requires_authentication']:
                self.assertEqual(response.status_code, 302, f"Access to core:{view_name} raised unexpected status code")
            else:
                self.assertEqual(response.status_code, 200, f"Access to core:{view_name} raised unexpected status code")
