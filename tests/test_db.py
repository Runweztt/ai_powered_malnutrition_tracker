import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch, MagicMock
from database.queries import save_user_data, load_user_history


class TestLoadUserHistory(unittest.TestCase):

    @patch("database.queries.get_connection")
    def test_returns_empty_list_for_unknown_user(self, mock_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = load_user_history("nobody")
        self.assertEqual(result, [])

    @patch("database.queries.get_connection")
    def test_returns_history_for_known_user(self, mock_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"id": 1}
        mock_cursor.fetchall.return_value = [
            {"recorded_at": "2025-01-01 10:00", "bmi_value": 22.5,
             "classification": "Normal", "calorie_target": 2000}
        ]
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = load_user_history("alice")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["classification"], "Normal")


class TestSaveUserData(unittest.TestCase):

    @patch("database.queries.get_connection")
    def test_save_commits_without_error(self, mock_conn):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"id": 1}
        mock_cursor.lastrowid = 5
        mock_conn.return_value.cursor.return_value = mock_cursor

        user_profile = {
            "username": "alice", "age": 28, "gender": "female",
            "activity_level": "moderate", "height_cm": 165.0, "weight_kg": 60.0
        }
        bmi_data = {"bmi_value": 22.04, "classification": "Normal", "calorie_target": 2000}

        save_user_data(user_profile, bmi_data, "Sample plan")
        mock_conn.return_value.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
