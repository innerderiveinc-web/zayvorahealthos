import sys
import os
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from tests.unit.verify_foundational_integrity import TestFoundationalIntegrity

__all__ = ["TestFoundationalIntegrity"]

if __name__ == "__main__":
    unittest.main()
