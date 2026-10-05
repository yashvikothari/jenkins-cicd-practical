import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import app

class AppTests(unittest.TestCase):
    def test_health_status_is_ok(self):
        payload = app.health_payload()
        self.assertEqual(payload["status"], "ok")

    def test_health_payload_contains_app_name(self):
        payload = app.health_payload()
        self.assertIn("app", payload)
        self.assertTrue(payload["app"])

    def test_health_payload_contains_environment(self):
        payload = app.health_payload()
        self.assertIn("environment", payload)

if __name__ == "__main__":
    unittest.main()
