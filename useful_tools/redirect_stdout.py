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

# usage:

### redirect to variable
########################
# with redirect_stdout() as out:
#     print("This will be captured")
#     print("So will this")
#
# Get the captured output
# output = out.getvalue()
# print(output)  # This will be captured\nSo will this\n
# print("This will not be captured")
# output = out.getvalue()
# print(output)  # This will be captured\nSo will this\n

### redirect to function
########################
# import contextlib
# class PrintNow():
#     def write(self, text):
#         # avoid printing the newline character twice
#         if text != "\n":
#             # Temporarily print directly to the original stdout, bypassing any redirection
#             original_stdout = sys.stdout  # Save the original stdout
#             sys.stdout = sys.__stdout__  # Temporarily disable redirection to make sure the message is printed to the console and not run through the PrintNow class, which would cause an infinite loop
#             print(f"captured text: {text}", flush=True)
#             sys.stdout = original_stdout
#     def flush(self):
#         # This method is required for compatibility with the file-like object.
#         pass
# with contextlib.redirect_stdout(PrintNow()):
#     print("This will be captured") # "captured text: This will be captured"

# print("This will not be captured")