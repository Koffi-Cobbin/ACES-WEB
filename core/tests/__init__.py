from django.test import SimpleTestCase
from django.urls import reverse


class TestView(SimpleTestCase):
    """
    Test that access to views that accept get do not raise exception.
    """
    def setUp(self) -> None:
        self.views = [
            {"name": 'index', 'requires_authentication': False},
        ]
        return super().setUp()

    def test_access_to_views(self):
        for view in self.views:
            print(view)
            view_name = view['name']
            response = self.client.get(reverse(f'core:{view_name}'))
            if view['requires_authentication']:
                self.assertEqual(response.status_code, 302, f"Access to core:{view_name} raised unexpected status code")
            else:
                self.assertEqual(response.status_code, 200, f"Access to core:{view_name} raised unexpected status code")
