"""Tests entry point. Just run the file to start tests."""

import unittest

if __name__ == "__main__":
    unittest.TextTestRunner().run(unittest.TestLoader().discover("."))
