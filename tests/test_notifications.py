import unittest
from datetime import date, timedelta
from src.notifications import generate_renewal_notifications

class TestNotifications(unittest.TestCase):

    def setUp(self):
        self.today = date(2024, 7, 15) # Fixed date for predictable tests
        # SWEET_SPOT_START_DAYS_BEFORE = 27
        # SWEET_SPOT_END_DAYS_BEFORE = 20

        self.policies = [
            { # In Window: 22 days from self.today (July 15 + 22 days = Aug 6)
                "insurance_type": "Car", "provider_name": "TestCar",
                "renewal_date": (self.today + timedelta(days=22)).strftime("%Y-%m-%d"),
            },
            { # Upcoming Window: 40 days from self.today
                "insurance_type": "Home", "provider_name": "TestHome",
                "renewal_date": (self.today + timedelta(days=40)).strftime("%Y-%m-%d"),
            },
            { # Past Renewal: 10 days ago
                "insurance_type": "Pet", "provider_name": "TestPet",
                "renewal_date": (self.today - timedelta(days=10)).strftime("%Y-%m-%d"),
            },
            { # In Window: 27 days from self.today (first day of window)
                "insurance_type": "Travel", "provider_name": "TestTravel",
                "renewal_date": (self.today + timedelta(days=27)).strftime("%Y-%m-%d"),
            },
            { # In Window: 20 days from self.today (last day of window)
                "insurance_type": "Gadget", "provider_name": "TestGadget",
                "renewal_date": (self.today + timedelta(days=20)).strftime("%Y-%m-%d"),
            },
            { # Invalid date, should be ignored
                "insurance_type": "Bike", "provider_name": "TestBike",
                "renewal_date": "NOT_A_DATE",
            },
            { # Missing renewal date, should be ignored
                "insurance_type": "Life", "provider_name": "TestLife",
            }
        ]

    def test_generate_renewal_notifications_in_window(self):
        notifications = generate_renewal_notifications(self.policies, self.today)
        self.assertEqual(len(notifications), 3) # Car, Travel, Gadget policies

        # Check content of one notification (e.g., TestCar)
        # Renewal date: 2024-07-15 + 22 days = 2024-08-06
        expected_msg_part_car = "REMINDER: Time to renew your Car policy with TestCar! Renewal is in 22 day(s) on 2024-08-06."

        found_car_notification = any(expected_msg_part_car in n for n in notifications)
        self.assertTrue(found_car_notification, "Car policy notification not found or incorrect.")

        # Check for Travel policy (first day of window)
        # Renewal date: 2024-07-15 + 27 days = 2024-08-11
        expected_msg_part_travel = "REMINDER: Time to renew your Travel policy with TestTravel! Renewal is in 27 day(s) on 2024-08-11."
        found_travel_notification = any(expected_msg_part_travel in n for n in notifications)
        self.assertTrue(found_travel_notification, "Travel policy notification not found or incorrect.")


    def test_generate_renewal_notifications_no_policies_in_window(self):
        # Create policies that are all outside the window
        policies_outside_window = [
            {
                "insurance_type": "Home", "provider_name": "TestHome",
                "renewal_date": (self.today + timedelta(days=40)).strftime("%Y-%m-%d"), # Upcoming
            },
            {
                "insurance_type": "Pet", "provider_name": "TestPet",
                "renewal_date": (self.today - timedelta(days=10)).strftime("%Y-%m-%d"), # Expired
            }
        ]
        notifications = generate_renewal_notifications(policies_outside_window, self.today)
        self.assertEqual(len(notifications), 0)

    def test_generate_renewal_notifications_empty_list(self):
        notifications = generate_renewal_notifications([], self.today)
        self.assertEqual(len(notifications), 0)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
