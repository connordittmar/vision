import os
import subprocess
import time
import unittest
from nose.tools import *
import vision

class VisionCliTestBase(unittest.TestCase):
    """Base for tests."""

    def setUp(self):
        """Setup vision client path and base args."""
        self.cli_path = os.path.join(
            os.path.dirname(__file__), "/vision/client.py")
        self.cli_base_args = [
            self.cli_path, '--url', 'http://10.17.163.109:8000', '--username',
            'testuser', '--password', 'testpass'
        ]

    def assertCliOk(self, args):
        """Determines that cli command succeeds."""
        self.assertEqual(0, subprocess.call(args))

class TestTargets(VisionCliTestBase):
    """Test able to upload targets."""

    def setUp(self):
        """Comput the testdata folder."""
        super(TestTargets, self).setUp()
        self.target_dir = os.path.join(os.path.dirname(__file__), "/bin/testdata")

    def test_upload_targets(self):
        """Test uploading targest with object file format."""
        self.assertCliOk(self.cli_base_args + [
            'targets', '--target_dir', self.target_dir
        ])

def main():
    tests = unittest.TestLoader().loadTestsFromTestCase(TestTargets)
    unittest.TextTestRunner(verbosity=3).run(tests)

if __name__ == '__main__':
    main()
