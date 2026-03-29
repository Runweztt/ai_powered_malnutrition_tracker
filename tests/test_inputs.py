import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from app.inputs import VALID_GENDERS, VALID_ACTIVITY


class TestInputConstants(unittest.TestCase):

    def test_valid_genders(self):
        self.assertIn("male", VALID_GENDERS)
        self.assertIn("female", VALID_GENDERS)

    def test_valid_activity_levels(self):
        self.assertIn("sedentary", VALID_ACTIVITY)
        self.assertIn("moderate",  VALID_ACTIVITY)
        self.assertIn("active",    VALID_ACTIVITY)

    def test_only_two_genders(self):
        self.assertEqual(len(VALID_GENDERS), 2)

    def test_only_three_activity_levels(self):
        self.assertEqual(len(VALID_ACTIVITY), 3)


if __name__ == "__main__":
    unittest.main()
