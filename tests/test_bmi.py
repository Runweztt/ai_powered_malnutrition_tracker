import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from app.bmi import calculate_bmi, classify_bmi
from app.calories import get_daily_calorie_target


class TestCalculateBMI(unittest.TestCase):

    def test_normal_bmi(self):
        bmi = calculate_bmi(70, 175)
        self.assertAlmostEqual(bmi, 22.86, places=1)

    def test_underweight(self):
        self.assertLess(calculate_bmi(45, 170), 18.5)

    def test_obese(self):
        self.assertGreaterEqual(calculate_bmi(110, 170), 30.0)

    def test_zero_height_raises(self):
        with self.assertRaises(ValueError):
            calculate_bmi(70, 0)

    def test_negative_weight_raises(self):
        with self.assertRaises(ValueError):
            calculate_bmi(-5, 170)


class TestClassifyBMI(unittest.TestCase):

    def test_underweight(self):
        self.assertEqual(classify_bmi(17.0), "Underweight")

    def test_normal(self):
        self.assertEqual(classify_bmi(22.0), "Normal")

    def test_overweight(self):
        self.assertEqual(classify_bmi(27.5), "Overweight")

    def test_obese(self):
        self.assertEqual(classify_bmi(35.0), "Obese")

    def test_boundary_normal_lower(self):
        self.assertEqual(classify_bmi(18.5), "Normal")

    def test_boundary_overweight(self):
        self.assertEqual(classify_bmi(25.0), "Overweight")

    def test_boundary_obese(self):
        self.assertEqual(classify_bmi(30.0), "Obese")


class TestCalorieTarget(unittest.TestCase):

    def test_returns_integer(self):
        self.assertIsInstance(get_daily_calorie_target("Normal", 25, "male", "moderate"), int)

    def test_underweight_higher_than_normal(self):
        normal = get_daily_calorie_target("Normal", 25, "male", "moderate")
        under  = get_daily_calorie_target("Underweight", 25, "male", "moderate")
        self.assertGreater(under, normal)

    def test_obese_lower_than_normal(self):
        normal = get_daily_calorie_target("Normal", 25, "male", "moderate")
        obese  = get_daily_calorie_target("Obese", 25, "male", "moderate")
        self.assertLess(obese, normal)

    def test_minimum_1200(self):
        self.assertGreaterEqual(
            get_daily_calorie_target("Obese", 80, "female", "sedentary"), 1200
        )


if __name__ == "__main__":
    unittest.main()
