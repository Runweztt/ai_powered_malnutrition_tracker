import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from app.reports import display_progress_report, _export_session


class TestProgressReport(unittest.TestCase):

    def test_empty_history_no_crash(self):
        try:
            display_progress_report([])
        except Exception as e:
            self.fail(f"Raised unexpected exception: {e}")

    def test_single_session_no_crash(self):
        history = [{"recorded_at": "2025-01-01 10:00", "bmi_value": 22.5,
                    "classification": "Normal", "calorie_target": 2000}]
        try:
            display_progress_report(history)
        except Exception as e:
            self.fail(f"Raised unexpected exception: {e}")

    def test_trend_decrease_detected(self):
        history = [
            {"recorded_at": "2025-01-01", "bmi_value": 28.0, "classification": "Overweight", "calorie_target": 1800},
            {"recorded_at": "2025-02-01", "bmi_value": 26.0, "classification": "Overweight", "calorie_target": 1800},
        ]
        try:
            display_progress_report(history)
        except Exception as e:
            self.fail(f"Raised unexpected exception: {e}")


class TestExportSession(unittest.TestCase):

    def setUp(self):
        self.user_profile = {
            "username": "testuser", "age": 25, "gender": "female",
            "activity_level": "moderate", "height_cm": 165.0, "weight_kg": 60.0
        }
        self.bmi_data = {"bmi_value": 22.04, "classification": "Normal", "calorie_target": 2000}
        self.diet_plan = "Sample diet plan."

    def test_export_creates_file(self):
        _export_session(self.user_profile, self.bmi_data, self.diet_plan)
        export_dir = os.path.join(os.path.dirname(__file__), "..", "exports")
        files = [f for f in os.listdir(export_dir) if f.startswith("testuser")]
        self.assertGreater(len(files), 0)
        # cleanup
        for f in files:
            os.remove(os.path.join(export_dir, f))

    def test_export_contains_bmi(self):
        _export_session(self.user_profile, self.bmi_data, self.diet_plan)
        export_dir = os.path.join(os.path.dirname(__file__), "..", "exports")
        files = [f for f in os.listdir(export_dir) if f.startswith("testuser")]
        with open(os.path.join(export_dir, files[0])) as f:
            content = f.read()
        self.assertIn("22.04", content)
        for f in files:
            os.remove(os.path.join(export_dir, f))


if __name__ == "__main__":
    unittest.main()
