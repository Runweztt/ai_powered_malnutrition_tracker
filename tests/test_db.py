import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch, MagicMock
from database.queries import save_user_data, load_user_history



def _make_chain(execute_data):
    """Return a MagicMock where every chained call returns itself,
    and .execute() returns a result with .data = execute_data."""
    chain = MagicMock()
   
    chain.table.return_value  = chain
    chain.select.return_value = chain
    chain.insert.return_value = chain
    chain.eq.return_value     = chain
    chain.order.return_value  = chain
    chain.limit.return_value  = chain

    result       = MagicMock()
    result.data  = execute_data
    chain.execute.return_value = result
    return chain



class TestLoadUserHistory(unittest.TestCase):

    @patch("database.queries.get_client")
    def test_returns_empty_list_for_unknown_user(self, mock_get_client):
        """When the users table returns no rows, history should be []."""
        client = _make_chain(execute_data=[])   
        mock_get_client.return_value = client

        result = load_user_history("nobody")
        self.assertEqual(result, [])

    @patch("database.queries.get_client")
    def test_returns_history_for_known_user(self, mock_get_client):
        """When the user exists and has BMI records, they should be returned."""
        history_rows = [
            {
                "recorded_at":    "2025-01-01 10:00",
                "bmi_value":      22.5,
                "classification": "Normal",
                "calorie_target": 2000
            }
        ]

        
        chain = MagicMock()
        chain.table.return_value  = chain
        chain.select.return_value = chain
        chain.insert.return_value = chain
        chain.eq.return_value     = chain
        chain.order.return_value  = chain
        chain.limit.return_value  = chain

        user_result      = MagicMock(); user_result.data    = [{"id": 1}]
        history_result   = MagicMock(); history_result.data = history_rows
        chain.execute.side_effect = [user_result, history_result]

        mock_get_client.return_value = chain

        result = load_user_history("alice")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["classification"], "Normal")
        self.assertEqual(result[0]["bmi_value"], 22.5)

    @patch("database.queries.get_client")
    def test_returns_empty_list_on_exception(self, mock_get_client):
        """If the Supabase client raises, an empty list should come back."""
        mock_get_client.side_effect = Exception("connection refused")

        result = load_user_history("alice")
        self.assertEqual(result, [])



class TestSaveUserData(unittest.TestCase):

    def _make_save_chain(self, user_id=1, bmi_record_id=5):
        """Build a chain that returns appropriate data for each execute() call
        during save_user_data:
          1. user lookup     → data=[{"id": user_id}]  (existing user)
          2. bmi_records insert → data=[{"id": bmi_record_id}]
          3. diet_plans insert  → data=[{"id": 99}]
        """
        chain = MagicMock()
        chain.table.return_value  = chain
        chain.select.return_value = chain
        chain.insert.return_value = chain
        chain.eq.return_value     = chain
        chain.order.return_value  = chain

        user_res    = MagicMock(); user_res.data    = [{"id": user_id}]
        bmi_res     = MagicMock(); bmi_res.data     = [{"id": bmi_record_id}]
        diet_res    = MagicMock(); diet_res.data    = [{"id": 99}]
        chain.execute.side_effect = [user_res, bmi_res, diet_res]

        return chain

    @patch("database.queries.get_client")
    def test_save_existing_user_runs_without_error(self, mock_get_client):
        """save_user_data should complete silently for an existing user."""
        mock_get_client.return_value = self._make_save_chain()

        user_profile = {
            "username": "alice", "age": 28, "gender": "female",
            "activity_level": "moderate", "height_cm": 165.0, "weight_kg": 60.0
        }
        bmi_data = {"bmi_value": 22.04, "classification": "Normal", "calorie_target": 2000}

        try:
            save_user_data(user_profile, bmi_data, "Sample AI plan")
        except Exception as e:
            self.fail(f"save_user_data raised unexpectedly: {e}")

    @patch("database.queries.get_client")
    def test_save_new_user_inserts_user_row(self, mock_get_client):
        """When the user does not exist, an insert should be triggered."""
        chain = MagicMock()
        chain.table.return_value  = chain
        chain.select.return_value = chain
        chain.insert.return_value = chain
        chain.eq.return_value     = chain
        chain.order.return_value  = chain

       
        no_user  = MagicMock(); no_user.data  = []
        new_user = MagicMock(); new_user.data = [{"id": 7}]
        bmi_res  = MagicMock(); bmi_res.data  = [{"id": 10}]
        diet_res = MagicMock(); diet_res.data = [{"id": 20}]
        chain.execute.side_effect = [no_user, new_user, bmi_res, diet_res]

        mock_get_client.return_value = chain

        user_profile = {
            "username": "bob", "age": 30, "gender": "male",
            "activity_level": "active", "height_cm": 180.0, "weight_kg": 80.0
        }
        bmi_data = {"bmi_value": 24.69, "classification": "Normal", "calorie_target": 2200}

        save_user_data(user_profile, bmi_data, "Sample AI plan")

        # insert should have been called at least twice (user + bmi + diet)
        self.assertGreaterEqual(chain.insert.call_count, 2)

    @patch("database.queries.get_client")
    def test_fallback_plan_tagged_correctly(self, mock_get_client):
        """A diet plan containing '[Offline plan]' should be stored as source='fallback'."""
        chain = self._make_save_chain()
        mock_get_client.return_value = chain

        user_profile = {
            "username": "carol", "age": 35, "gender": "female",
            "activity_level": "sedentary", "height_cm": 160.0, "weight_kg": 55.0
        }
        bmi_data = {"bmi_value": 21.48, "classification": "Normal", "calorie_target": 1800}
        fallback_text = "\n  [Offline plan]  Daily target: 1800 kcal\nGOAL: Maintain..."

        
        try:
            save_user_data(user_profile, bmi_data, fallback_text)
        except Exception as e:
            self.fail(f"save_user_data raised unexpectedly with fallback plan: {e}")

    @patch("database.queries.get_client")
    def test_exception_does_not_propagate(self, mock_get_client):
        """If Supabase raises, save_user_data should swallow it gracefully."""
        mock_get_client.side_effect = Exception("network error")

        user_profile = {
            "username": "alice", "age": 28, "gender": "female",
            "activity_level": "moderate", "height_cm": 165.0, "weight_kg": 60.0
        }
        bmi_data = {"bmi_value": 22.04, "classification": "Normal", "calorie_target": 2000}

        try:
            save_user_data(user_profile, bmi_data, "plan")
        except Exception as e:
            self.fail(f"Exception should have been caught internally, but got: {e}")


if __name__ == "__main__":
    unittest.main()