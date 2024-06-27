from datetime import datetime, timezone

# consistenly using this (and thus not needing to import datetime) has these benefits:
# - current time can be mocked in tests
# - can prevent accidentally using the local time instead of UTC

def get_current_utc_time():
    """return the current time in UTC, with tz info removed, so it can be compared to other datetimes"""
    return datetime.now(timezone.utc).replace(tzinfo=None)
