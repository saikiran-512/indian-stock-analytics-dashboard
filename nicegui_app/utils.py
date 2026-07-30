import datetime

def format_currency(value):
    if value is None:
        return "N/A"
    return f"₹{value:,.2f}"

def format_large_number(value):
    if value is None:
        return "N/A"
    if value >= 1_000_000_000_000:
        return f"₹{value / 1_000_000_000_000:.2f}T"
    if value >= 1_000_000_000:
        return f"₹{value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"₹{value / 1_000_000:.2f}M"
    return f"₹{value:,.0f}"

def format_percentage(value):
    if value is None:
        return "N/A"
    return f"{value:.2f}%"

def get_current_date_time():
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y - %I:%M %p")
