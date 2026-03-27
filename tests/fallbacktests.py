
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fallback_diet import get_fallback_diet_plan
from ai_diet import generate_diet_plan


# ──────────────────────────────────────────────────────────────────────────────
# Fallback diet tests
# ──────────────────────────────────────────────────────────────────────────────

class TestFallbackDietPlan(unittest.TestCase):

    VALID_CLASSIFICATIONS = ["Underweight", "Normal", "Overweight", "Obese"]

    def test_returns_dict_for_all_classifications(self):
        for cls in self.VALID_CLASSIFICATIONS:
            with self.subTest(classification=cls):
                plan = get_fallback_diet_plan(cls)
                self.assertIsInstance(plan, dict)

    def test_required_keys_present(self):
        required = {"source", "macros", "meals", "prioritise",
                    "avoid", "hydration", "lifestyle_tip"}
        for cls in self.VALID_CLASSIFICATIONS:
            with self.subTest(classification=cls):
                plan = get_fallback_diet_plan(cls)
                self.assertTrue(required.issubset(plan.keys()))

    def test_source_is_offline_fallback(self):
        for cls in self.VALID_CLASSIFICATIONS:
            plan = get_fallback_diet_plan(cls)
            self.assertEqual(plan["source"], "Offline Fallback")

    def test_macros_contain_three_keys(self):
        for cls in self.VALID_CLASSIFICATIONS:
            plan = get_fallback_diet_plan(cls)
            self.assertIn("carbohydrates", plan["macros"])
            self.assertIn("protein", plan["macros"])
            self.assertIn("fats", plan["macros"])

    def test_meals_contain_five_entries(self):
        expected_meals = {
            "Breakfast", "Morning Snack", "Lunch",
            "Afternoon Snack", "Dinner"
        }
        for cls in self.VALID_CLASSIFICATIONS:
            plan = get_fallback_diet_plan(cls)
            self.assertEqual(set(plan["meals"].keys()), expected_meals)

    def test_prioritise_and_avoid_are_lists(self):
        for cls in self.VALID_CLASSIFICATIONS:
            plan = get_fallback_diet_plan(cls)
            self.assertIsInstance(plan["prioritise"], list)
            self.assertIsInstance(plan["avoid"], list)

    def test_unknown_classification_returns_default(self):
        plan = get_fallback_diet_plan("Unknown")
        self.assertIsInstance(plan, dict)
        self.assertIn("lifestyle_tip", plan)


# ──────────────────────────────────────────────────────────────────────────────
# AI diet generation tests (Claude API mocked)
# ──────────────────────────────────────────────────────────────────────────────

_MOCK_RESPONSE_TEXT = """\
MACROS:
Carbohydrates: 45%
Protein: 30%
Fats: 25%

MEALS:
Breakfast: Oatmeal with berries
Morning Snack: Greek yoghurt
Lunch: Grilled chicken salad
Afternoon Snack: Apple
Dinner: Baked salmon with vegetables

PRIORITISE:
- Vegetables
- Lean protein
- Whole grains
- Fruits
- Healthy fats

AVOID:
- Sugary drinks
- Fried food
- Processed snacks
- Alcohol

HYDRATION:
Drink 2 litres of water per day.

LIFESTYLE TIP:
Aim for 30 minutes of moderate exercise daily.
"""

_SAMPLE_PROFILE = {
    "name": "Jane",
    "age": 28,
    "gender": "female",
    "height_cm": 165,
    "weight_kg": 65,
    "activity_level": "moderate",
    "bmi": 23.88,
    "bmi_classification": "Normal",
    "daily_calorie_target": 2000,
}


class TestGenerateDietPlan(unittest.TestCase):

    def _mock_client(self):
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text=_MOCK_RESPONSE_TEXT)]
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_msg
        return mock_client

    @patch("ai_diet.anthropic.Anthropic")
    def test_successful_api_call_returns_dict(self, mock_anthropic):
        mock_anthropic.return_value = self._mock_client()
        plan = generate_diet_plan(_SAMPLE_PROFILE)
        self.assertIsInstance(plan, dict)

    @patch("ai_diet.anthropic.Anthropic")
    def test_source_is_claude_ai_on_success(self, mock_anthropic):
        mock_anthropic.return_value = self._mock_client()
        plan = generate_diet_plan(_SAMPLE_PROFILE)
        self.assertEqual(plan["source"], "Claude AI")

    @patch("ai_diet.anthropic.Anthropic")
    def test_macros_parsed_correctly(self, mock_anthropic):
        mock_anthropic.return_value = self._mock_client()
        plan = generate_diet_plan(_SAMPLE_PROFILE)
        self.assertEqual(plan["macros"]["carbohydrates"], "45%")
        self.assertEqual(plan["macros"]["protein"], "30%")
        self.assertEqual(plan["macros"]["fats"], "25%")

    @patch("ai_diet.anthropic.Anthropic")
    def test_five_meals_parsed(self, mock_anthropic):
        mock_anthropic.return_value = self._mock_client()
        plan = generate_diet_plan(_SAMPLE_PROFILE)
        self.assertEqual(len(plan["meals"]), 5)

    @patch("ai_diet.anthropic.Anthropic")
    def test_prioritise_list_not_empty(self, mock_anthropic):
        mock_anthropic.return_value = self._mock_client()
        plan = generate_diet_plan(_SAMPLE_PROFILE)
        self.assertGreater(len(plan["prioritise"]), 0)

    @patch("ai_diet.anthropic.Anthropic")
    def test_api_connection_error_falls_back(self, mock_anthropic):
        import anthropic as anthropic_lib
        mock_anthropic.return_value.messages.create.side_effect = (
            anthropic_lib.APIConnectionError(request=MagicMock())
        )
        plan = generate_diet_plan(_SAMPLE_PROFILE)
        self.assertEqual(plan["source"], "Offline Fallback")

    @patch("ai_diet.anthropic.Anthropic")
    def test_auth_error_falls_back(self, mock_anthropic):
        import anthropic as anthropic_lib
        mock_anthropic.return_value.messages.create.side_effect = (
            anthropic_lib.AuthenticationError(
                message="bad key", response=MagicMock(), body={}
            )
        )
        plan = generate_diet_plan(_SAMPLE_PROFILE)
        self.assertEqual(plan["source"], "Offline Fallback")


if __name__ == "__main__":
    unittest.main()
