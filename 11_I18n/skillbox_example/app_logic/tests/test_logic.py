from django.test import SimpleTestCase

from app_logic.helpers import check_access_by_age


class BusinessLogicTest(SimpleTestCase):
    def test_access_denied(self):
        self.assertTrue(check_access_by_age(17))

    def test_access_denied(self):
            self.assertEqual(check_access_by_age(17), True)
