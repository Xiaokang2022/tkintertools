"""Tests entry point

Use `python -m tests` or run the file directly to test
"""

import unittest

if __name__ == "__main__":
    unittest.TextTestRunner().run(unittest.TestLoader().discover("."))
