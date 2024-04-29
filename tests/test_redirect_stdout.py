import unittest
from useful_tools.redirect_stdout import redirect_stdout

class TestRedirectStdout(unittest.TestCase):
    def test_redirect_stdout(self):
        with redirect_stdout() as output:
            print("Test message")

        output_string = output.getvalue()
        self.assertEqual(output_string, "Test message\n")

if __name__ == '__main__':
    unittest.main()