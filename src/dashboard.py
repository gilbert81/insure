from datetime import date, timedelta # Added timedelta
from src.pdf_parser import process_pdf_to_structured_data # Mock version for now
from src.renewal_engine import parse_renewal_date, get_renewal_status_and_countdown

def format_policy_card(policy_data: dict, renewal_info: dict) -> str:
    """Formats a single policy into a CLI card string."""
    card_lines = [
        "-----------------------------------------------------",
        f"| {policy_data.get('insurance_type', 'N/A')} Insurance • Provider: {policy_data.get('provider_name', 'N/A')}",
    ]

    renewal_date_str = policy_data.get('renewal_date', 'N/A')
    status_message = renewal_info.get('message', 'Could not determine renewal status.')
    days_to_renewal = renewal_info.get('days_to_renewal')
    renewal_status_indicator = renewal_info.get('status', '')

    # Simplified status indicator for CLI
    cli_status_indicator = ""
    if renewal_status_indicator == "In Window":
        cli_status_indicator = "🟢 (Ideal window)"
    elif renewal_status_indicator == "Upcoming Window":
        cli_status_indicator = "🔵 (Upcoming)"
    elif renewal_status_indicator == "Past Window":
        cli_status_indicator = "🟠 (Window passed)"
    elif renewal_status_indicator == "Past Renewal":
        cli_status_indicator = "🔴 (Expired)"

    if days_to_renewal is not None:
        renewal_line = f"| Renewal: {renewal_date_str} • {days_to_renewal} days left {cli_status_indicator}"
    else:
        renewal_line = f"| Renewal: {renewal_date_str} {cli_status_indicator}"

    card_lines.append(renewal_line)
    card_lines.append(f"| Status: {status_message}")

    card_lines.append(
        f"| £{policy_data.get('premium_amount', 'N/A')} • {policy_data.get('coverage_type', 'N/A')} • £{policy_data.get('excess_amount', 'N/A')} excess"
    )
    card_lines.append(f"| [Start getting quotes] (Dummy Button)")
    card_lines.append("-----------------------------------------------------")
    return "\n".join(card_lines)

def display_dashboard(policy_files: list[str], current_date: date):
    """
    Processes policy PDFs and displays them on a CLI dashboard.
    policy_files: A list of paths to PDF files.
    """
    print("\n======= INSURANCE DASHBOARD =======")
    if not policy_files:
        print("No policies to display.")
        return

    for pdf_file_path in policy_files:
        print(f"\nProcessing: {pdf_file_path}...")
        policy_data = process_pdf_to_structured_data(pdf_file_path) # Uses mock LLM

        if not policy_data:
            print(f"Could not extract data from {pdf_file_path}")
            continue

        renewal_date_obj = parse_renewal_date(policy_data.get("renewal_date"))
        renewal_info = get_renewal_status_and_countdown(renewal_date_obj, current_date)

        card_str = format_policy_card(policy_data, renewal_info)
        print(card_str)

        # Display renewal engine's savings tip
        if renewal_info.get("savings_tip"):
            print(f"| Tip: {renewal_info['savings_tip']}")
            print("-----------------------------------------------------")


if __name__ == '__main__':
    # Ensure 'data/example_document_for_parsing.pdf' exists for this example to work.
    # The pdf_parser's mock LLM will determine what data is extracted.
    # The renewal_engine will calculate status based on that.

    # Create a dummy policy file for testing if it doesn't exist
    # This is just to make the __main__ runnable without external setup.
    import os
    dummy_pdf_path = 'data/example_document_for_parsing.pdf'
    if not os.path.exists(dummy_pdf_path):
        print(f"Warning: {dummy_pdf_path} not found. Dashboard example may not show full data.")
        # To make it runnable, we might create a dummy file or skip.
        # For now, it will proceed and likely show "Could not extract data".
        # In a real scenario, this file must exist.
        # Fallback: create a dummy file so pdf_parser doesn't fail on file open
        # if not os.path.exists('data'): os.makedirs('data')
        # with open(dummy_pdf_path, 'w') as f: f.write("dummy content")

    policy_pdf_list = [dummy_pdf_path]

    # You can add more dummy PDFs to this list if you have them.
    # For example, if you had 'data/another_policy.pdf':
    # policy_pdf_list.append('data/another_policy.pdf')

    today = date.today()
    display_dashboard(policy_pdf_list, today)

    # --- DEMONSTRATE NOTIFICATIONS ---
    # This part would typically be in a main application orchestrator.
    # We need to re-process or pass the policy data to the notification system.
    # For simplicity, let's re-process the example PDF for notification check.

    print("\n\n--- Checking for Notifications ---")
    # We need the structured data, not just the file paths.
    # Let's assume we have a list of policy data dicts.
    # We'll re-use the process_pdf_to_structured_data for the example PDF.

    all_policy_data_for_notifications = []
    if os.path.exists(dummy_pdf_path): # dummy_pdf_path is defined earlier in dashboard.py's main
        policy_struct_data = process_pdf_to_structured_data(dummy_pdf_path)
        if policy_struct_data:
            all_policy_data_for_notifications.append(policy_struct_data)

    # Example: Add another policy manually for notification testing
    # This policy should be "In Window" for today's date for the notification to trigger
    # from datetime import timedelta # timedelta is now imported at the top
    manual_policy_in_window = {
        "insurance_type": "ManualTest", "provider_name": "NotifyMe",
        "renewal_date": (today + timedelta(days=23)).strftime("%Y-%m-%d"), # Should be in window
    }
    all_policy_data_for_notifications.append(manual_policy_in_window)

    if all_policy_data_for_notifications:
        from src.notifications import generate_renewal_notifications # Import here
        active_notifications = generate_renewal_notifications(all_policy_data_for_notifications, today)
        if active_notifications:
            print("🔔 You have active renewal reminders: 🔔")
            for notif_msg in active_notifications:
                print(f"  - {notif_msg}")
        else:
            print("No policies are currently in the renewal sweet spot for notification.")
    else:
        print("No policy data available to check for notifications.")
