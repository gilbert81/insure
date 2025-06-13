from datetime import date, timedelta # Added timedelta here for the __main__ block
from src.renewal_engine import parse_renewal_date, get_renewal_status_and_countdown

def generate_renewal_notifications(policy_data_list: list[dict], current_date: date) -> list[str]:
    """
    Checks policies and generates notification messages for those in the renewal sweet spot.

    Args:
        policy_data_list: A list of dictionaries, where each dictionary is structured policy data.
                          (Assumes structure from pdf_parser.process_pdf_to_structured_data)
        current_date: The current date to check against.

    Returns:
        A list of notification strings for policies in the sweet spot.
    """
    notifications = []
    for policy in policy_data_list:
        renewal_date_str = policy.get("renewal_date")
        renewal_date_obj = parse_renewal_date(renewal_date_str)

        if not renewal_date_obj:
            # Cannot process notification for this policy if date is invalid
            continue

        renewal_info = get_renewal_status_and_countdown(renewal_date_obj, current_date)

        if renewal_info.get("status") == "In Window":
            provider = policy.get("provider_name", "your provider")
            insurance_type = policy.get("insurance_type", "Your insurance")
            days_to_renewal = renewal_info.get("days_to_renewal", "soon")

            message = (
                f"🔔 REMINDER: Time to renew your {insurance_type} policy with {provider}! "
                f"Renewal is in {days_to_renewal} day(s) on {renewal_date_obj.strftime('%Y-%m-%d')}. "
                f"You're in the optimal window to find the best quotes."
            )
            notifications.append(message)

    return notifications

if __name__ == '__main__':
    # Example Usage:
    today = date.today()

    # Sample policy data (mimicking output from pdf_parser)
    sample_policies = [
        {
            "insurance_type": "Car", "provider_name": "AutoInsure",
            "renewal_date": (today + timedelta(days=22)).strftime("%Y-%m-%d"), # In window
            "premium_amount": "600", "coverage_type": "Comprehensive", "excess_amount": "300"
        },
        {
            "insurance_type": "Home", "provider_name": "HomeSecure",
            "renewal_date": (today + timedelta(days=45)).strftime("%Y-%m-%d"), # Upcoming
            "premium_amount": "400", "coverage_type": "Standard", "excess_amount": "500"
        },
        {
            "insurance_type": "Travel", "provider_name": "WorldNomad",
            "renewal_date": (today + timedelta(days=25)).strftime("%Y-%m-%d"), # In window
            "premium_amount": "100", "coverage_type": "Multi-trip", "excess_amount": "100"
        },
        { # Policy with invalid date for notification processing
            "insurance_type": "Pet", "provider_name": "PetWell",
            "renewal_date": "invalid-date-format",
        }
    ]

    # No need to re-import timedelta, it's at the top of the file now.

    print("Checking for renewal notifications...")
    active_notifications = generate_renewal_notifications(sample_policies, today)

    if active_notifications:
        print("\n=== Renewal Reminders ===")
        for notif in active_notifications:
            print(f"- {notif}")
    else:
        print("\nNo policies currently require renewal reminders.")
