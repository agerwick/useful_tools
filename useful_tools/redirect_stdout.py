import sys
from io import StringIO
from contextlib import contextmanager

@contextmanager
def redirect_stdout():
    # Create a temporary variable to hold the output
    temp_out = StringIO()

    # Save the current stdout so we can restore it later
    old_stdout = sys.stdout

    # Redirect stdout to our temporary variable
    sys.stdout = temp_out

    try:
        yield temp_out
    finally:
        # Restore stdout to its original value
        sys.stdout = old_stdout
