import sys
import os
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from tests.verify_all_prompts_1_to_28 import TestAllPrompts1To28Acceptance

__all__ = ["TestAllPrompts1To28Acceptance"]

if __name__ == "__main__":
    unittest.main()
