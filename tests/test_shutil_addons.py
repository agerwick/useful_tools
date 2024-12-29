import unittest
from unittest.mock import patch
import os
import stat
from useful_tools.shutil_addons import shutil, original_shutil

class TestShutilAddons(unittest.TestCase):

    def test_rmtree_force(self):
        folder = 'cache/rmtree_force_test'
        # create a random directories
        os.makedirs(folder, exist_ok=True)
        os.makedirs(folder + '/subdir', exist_ok=True)
        os.makedirs(folder + '/subdir/subsubdir', exist_ok=True)
        # create a random file
        with open(folder + '/subdir/subsubdir/file.txt', 'w') as f:
            f.write('test')
        # make the file read-only
        os.chmod(folder + '/subdir/subsubdir/file.txt', stat.S_IRUSR)
        # Call the function
        shutil.rmtree_force(folder)
        # Verify that the directory was deleted
        self.assertFalse(os.path.exists(folder))

if __name__ == '__main__':
    unittest.main()
