import unittest
from unittest.mock import patch
from io import StringIO
from datetime import date
from src.dashboard import format_policy_card, display_dashboard

class TestDashboard(unittest.TestCase):

    def test_format_policy_card(self):
        policy_data = {
            "insurance_type": "Car", "provider_name": "TestInsure",
            "renewal_date": "2024-12-25", "premium_amount": "500",
            "coverage_type": "Comprehensive", "excess_amount": "250"
        }
        renewal_info = {
            "status": "Upcoming Window",
            "message": "Ideal renewal window starts in 10 day(s).",
            "days_to_renewal": 40, # Example
            "window_start_date": "2024-12-05",
            "window_end_date": "2024-12-15",
            "renewal_date": "2024-12-25",
            "savings_tip": "Save money by renewing early!"
        }

        card_str = format_policy_card(policy_data, renewal_info)

        self.assertIn("Car Insurance • Provider: TestInsure", card_str)
        self.assertIn("Renewal: 2024-12-25 • 40 days left 🔵 (Upcoming)", card_str)
        self.assertIn("Status: Ideal renewal window starts in 10 day(s).", card_str)
        self.assertIn("£500 • Comprehensive • £250 excess", card_str)
        self.assertIn("[Start getting quotes] (Dummy Button)", card_str)

    def test_format_policy_card_missing_data(self):
        policy_data = {"insurance_type": "Home"} # Most data missing
        renewal_info = {"status": "Invalid Date", "message": "Date missing."}

        card_str = format_policy_card(policy_data, renewal_info)
        self.assertIn("Home Insurance • Provider: N/A", card_str)
        self.assertIn("Renewal: N/A", card_str) # No date, no days left
        self.assertIn("Status: Date missing.", card_str)
        self.assertIn("£N/A • N/A • £N/A excess", card_str)


    @patch('src.dashboard.process_pdf_to_structured_data')
    @patch('src.dashboard.parse_renewal_date')
    @patch('src.dashboard.get_renewal_status_and_countdown')
    @patch('sys.stdout', new_callable=StringIO) # Capture prints
    def test_display_dashboard_single_policy(self, mock_stdout, mock_renewal_status, mock_parse_date, mock_process_pdf):
        # Mock return values
        mock_process_pdf.return_value = {
            "insurance_type": "Test Policy", "provider_name": "MockProvider",
            "renewal_date": "2025-01-15", "premium_amount": "100",
            "coverage_type": "Basic", "excess_amount": "50"
        }
        mock_parse_date.return_value = date(2025, 1, 15)
        mock_renewal_status.return_value = {
            "status": "In Window",
            "message": "You are in the ideal window!",
            "days_to_renewal": 25,
            "savings_tip": "Mock tip."
        }

        # Dummy PDF path for the test
        test_pdf_files = ["dummy_policy.pdf"]
        today = date(2024, 12, 21) # Fixed date for test

        display_dashboard(test_pdf_files, today)

        output = mock_stdout.getvalue()

        mock_process_pdf.assert_called_once_with("dummy_policy.pdf")
        mock_parse_date.assert_called_once_with("2025-01-15")
        mock_renewal_status.assert_called_once_with(date(2025, 1, 15), today)

        self.assertIn("======= INSURANCE DASHBOARD =======", output)
        self.assertIn("Processing: dummy_policy.pdf...", output)
        self.assertIn("Test Policy Insurance • Provider: MockProvider", output)
        self.assertIn("Renewal: 2025-01-15 • 25 days left 🟢 (Ideal window)", output)
        self.assertIn("Status: You are in the ideal window!", output)
        self.assertIn("£100 • Basic • £50 excess", output)
        self.assertIn("[Start getting quotes] (Dummy Button)", output)
        self.assertIn("Tip: Mock tip.", output)

    @patch('src.dashboard.process_pdf_to_structured_data')
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_dashboard_no_data_extracted(self, mock_stdout, mock_process_pdf):
        mock_process_pdf.return_value = None # Simulate failure to extract

        test_pdf_files = ["failed_extraction.pdf"]
        today = date(2024,1,1)
        display_dashboard(test_pdf_files, today)
        output = mock_stdout.getvalue()

        self.assertIn("Could not extract data from failed_extraction.pdf", output)
        # Ensure no card formatting is attempted if data extraction fails
        self.assertNotIn("Provider:", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_dashboard_no_policies(self, mock_stdout):
        display_dashboard([], date.today())
        output = mock_stdout.getvalue()
        self.assertIn("No policies to display.", output)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
