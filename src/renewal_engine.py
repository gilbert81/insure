from datetime import datetime, timedelta, date

# Constants for renewal sweet spot (as per PRD)
SWEET_SPOT_START_DAYS_BEFORE = 27
SWEET_SPOT_END_DAYS_BEFORE = 20

def parse_renewal_date(date_str: str | None) -> date | None:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def get_renewal_window(renewal_date: date | None) -> tuple[date, date] | None:
    if not renewal_date:
        return None
    window_start = renewal_date - timedelta(days=SWEET_SPOT_START_DAYS_BEFORE)
    window_end = renewal_date - timedelta(days=SWEET_SPOT_END_DAYS_BEFORE)
    return window_start, window_end

def get_renewal_status_and_countdown(renewal_date: date | None, current_date: date) -> dict:
    if not renewal_date:
        return {
            "status": "Invalid Date", "message": "Renewal date is missing or invalid.",
            "days_to_renewal": None, "days_to_window_start": None,
            "window_start_date": None, "window_end_date": None,
            "renewal_date": None, "savings_tip": None
        }

    parsed_renewal_dt = renewal_date
    window_info = get_renewal_window(parsed_renewal_dt)
    if not window_info: # Should ideally not be hit if renewal_date is valid
        return {
            "status": "Error", "message": "Could not calculate renewal window.",
            "renewal_date": parsed_renewal_dt.strftime("%Y-%m-%d"),
            "days_to_renewal": None, "days_to_window_start": None,
            "window_start_date": None, "window_end_date": None, "savings_tip": None
        }
    window_start, window_end = window_info

    days_to_renewal = (parsed_renewal_dt - current_date).days
    days_to_window_start = (window_start - current_date).days
    days_to_window_end = (window_end - current_date).days

    status = ""
    message = ""

    if days_to_renewal < 0:
        status = "Past Renewal"
        message = f"Policy renewal date ({parsed_renewal_dt.strftime('%Y-%m-%d')}) has passed."
    elif current_date >= window_start and current_date <= window_end:
        status = "In Window"
        message = f"You are in the ideal renewal window! It ends in {days_to_window_end} day(s) on {window_end.strftime('%Y-%m-%d')}."
        message += f" Renewal is in {days_to_renewal} day(s)."
    elif current_date < window_start:
        status = "Upcoming Window"
        message = f"Ideal renewal window starts in {days_to_window_start} day(s) (from {window_start.strftime('%Y-%m-%d')} to {window_end.strftime('%Y-%m-%d')})."
        message += f" Renewal is in {days_to_renewal} day(s)."
    else: # current_date > window_end (but renewal not yet passed)
        status = "Past Window"
        message = f"The ideal renewal window ({window_start.strftime('%Y-%m-%d')} to {window_end.strftime('%Y-%m-%d')}) has passed."
        message += f" Renewal is in {days_to_renewal} day(s). Consider acting soon."

    savings_tip = "Users renewing around 23-26 days early often save money compared to last-minute renewals."

    return {
        "status": status, "message": message,
        "days_to_renewal": days_to_renewal,
        "days_to_window_start": days_to_window_start if current_date < window_start else 0,
        "window_start_date": window_start.strftime("%Y-%m-%d"),
        "window_end_date": window_end.strftime("%Y-%m-%d"),
        "renewal_date": parsed_renewal_dt.strftime("%Y-%m-%d"),
        "savings_tip": savings_tip
    }

if __name__ == '__main__':
    today = date.today()
    print("Renewal Engine - Example for a renewal 30 days from today:")
    example_renewal_date = parse_renewal_date((today + timedelta(days=30)).strftime("%Y-%m-%d"))
    if example_renewal_date:
        status_info = get_renewal_status_and_countdown(example_renewal_date, today)
        for key, value in status_info.items():
            print(f"  {key}: {value}")
    else:
        print("Could not parse example renewal date.")
