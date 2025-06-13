import unittest
from datetime import date, timedelta
from src.renewal_engine import (
    parse_renewal_date,
    get_renewal_window,
    get_renewal_status_and_countdown,
    SWEET_SPOT_START_DAYS_BEFORE,
    SWEET_SPOT_END_DAYS_BEFORE
)

class TestRenewalEngine(unittest.TestCase):

    def test_parse_renewal_date(self):
        self.assertEqual(parse_renewal_date("2024-08-15"), date(2024, 8, 15))
        self.assertIsNone(parse_renewal_date("invalid-date"))
        self.assertIsNone(parse_renewal_date("2024/08/15"))
        self.assertIsNone(parse_renewal_date(None)) # type: ignore
        self.assertIsNone(parse_renewal_date(""))

    def test_get_renewal_window(self):
        renewal_dt = date(2024, 8, 15)
        expected_start = renewal_dt - timedelta(days=SWEET_SPOT_START_DAYS_BEFORE)
        expected_end = renewal_dt - timedelta(days=SWEET_SPOT_END_DAYS_BEFORE)
        self.assertEqual(get_renewal_window(renewal_dt), (expected_start, expected_end))
        self.assertIsNone(get_renewal_window(None))

    def test_get_renewal_status_and_countdown(self):
        today = date(2024, 7, 15)

        renewal_dt_upcoming = today + timedelta(days=60)
        status_upcoming = get_renewal_status_and_countdown(renewal_dt_upcoming, today)
        self.assertEqual(status_upcoming["status"], "Upcoming Window")
        self.assertTrue(status_upcoming["message"].startswith("Ideal renewal window starts in"))
        self.assertEqual(status_upcoming["renewal_date"], renewal_dt_upcoming.strftime("%Y-%m-%d"))
        self.assertTrue(status_upcoming["days_to_window_start"] > 0)

        renewal_dt_in_window = today + timedelta(days=SWEET_SPOT_END_DAYS_BEFORE + 2)
        status_in_window = get_renewal_status_and_countdown(renewal_dt_in_window, today)
        self.assertEqual(status_in_window["status"], "In Window")
        self.assertTrue(status_in_window["message"].startswith("You are in the ideal renewal window!"))
        self.assertEqual(status_in_window["days_to_window_start"], 0)

        renewal_dt_past = today - timedelta(days=10)
        status_past = get_renewal_status_and_countdown(renewal_dt_past, today)
        self.assertEqual(status_past["status"], "Past Renewal")
        self.assertTrue(status_past["message"].endswith("has passed."))

        renewal_dt_past_window = today + timedelta(days=10)
        status_past_window = get_renewal_status_and_countdown(renewal_dt_past_window, today)
        self.assertEqual(status_past_window["status"], "Past Window")
        self.assertTrue(status_past_window["message"].startswith("The ideal renewal window"))
        self.assertTrue("Consider acting soon" in status_past_window["message"])

        status_invalid_date = get_renewal_status_and_countdown(None, today)
        self.assertEqual(status_invalid_date["status"], "Invalid Date")
        self.assertEqual(status_invalid_date["message"], "Renewal date is missing or invalid.")
        self.assertIsNone(status_invalid_date["renewal_date"])
        self.assertIsNone(status_invalid_date["savings_tip"])

    def test_renewal_status_edge_cases_window_boundaries(self):
        today = date(2024, 7, 15)

        renewal_dt_window_start_day = today + timedelta(days=SWEET_SPOT_START_DAYS_BEFORE)
        status_on_start = get_renewal_status_and_countdown(renewal_dt_window_start_day, today)
        self.assertEqual(status_on_start["status"], "In Window",
                            f"Should be 'In Window' on the first day. Days to renewal: {status_on_start['days_to_renewal']}")

        renewal_dt_window_end_day = today + timedelta(days=SWEET_SPOT_END_DAYS_BEFORE)
        status_on_end = get_renewal_status_and_countdown(renewal_dt_window_end_day, today)
        self.assertEqual(status_on_end["status"], "In Window",
                            f"Should be 'In Window' on the last day. Days to renewal: {status_on_end['days_to_renewal']}")

        renewal_dt_before_window = today + timedelta(days=SWEET_SPOT_START_DAYS_BEFORE + 1)
        status_before = get_renewal_status_and_countdown(renewal_dt_before_window, today)
        self.assertEqual(status_before["status"], "Upcoming Window", "Should be 'Upcoming Window' day before start")
        self.assertEqual(status_before["days_to_window_start"], 1)

        renewal_dt_after_window = today + timedelta(days=SWEET_SPOT_END_DAYS_BEFORE - 1)
        status_after = get_renewal_status_and_countdown(renewal_dt_after_window, today)
        self.assertEqual(status_after["status"], "Past Window", "Should be 'Past Window' day after end")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
