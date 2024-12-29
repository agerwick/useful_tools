"""
This module extends the shutil module with a new function rmtree_force that deletes a directory and all its contents, even if some files are read-only.
"""

import shutil as original_shutil
import os
import stat

# Function to handle errors during rmtree
def _handle_remove_readonly(func, path, exc):
    if func in (os.rmdir, os.remove, os.unlink) and isinstance(exc, PermissionError):
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise exc # pragma: no cover

def _rmtree_force(dir):
    original_shutil.rmtree(dir, onexc=_handle_remove_readonly)

class ShutilExtended:
    def __getattr__(self, name):
        return getattr(original_shutil, name)

    def rmtree_force(self, dir):
        _rmtree_force(dir)

shutil = ShutilExtended()

# usage:
# from useful_tools.shutil_addons import shutil
# shutil.rmtree_force('path/to/directory')
# shutil.copy('source', 'destination')
# shutil.move('source', 'destination')
# etc.
