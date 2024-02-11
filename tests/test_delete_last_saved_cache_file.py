import os
from useful_tools.cache_to_disk import cache_to_disk

class MyClass:
    cache_enabled = True
    cache_dir = "test_cache"
    cache_expiration = 2
    force_cache_expiration = False
    ignore_cache_expiration = False

    def __init__(self):
        pass
        #self.last_saved_cache_file = "cache_file.txt"

    @cache_to_disk # this will define delete_last_saved_cache_file on the class
    def dummy(self, *args, **kwargs):
        return (self, args, kwargs)


def test_delete_last_saved_cache_file():
    my_class = MyClass()
    my_class.force_cache_expiration = True # force cache expiration, so any existing cache file will be deleted
    my_class.dummy("test_delete_last_saved_cache_file") # this will create a cache file
    cache_file = my_class.cache_status_dict["last_saved_cache_file"]
    assert os.path.exists(cache_file) # check that file exists
    assert cache_file == my_class.delete_last_saved_cache_file() # delete the cache file
    assert not os.path.exists(cache_file) # Check if the cache file is actually deleted

def test_delete_last_saved_cache_file_with_non_existent_file():
    my_class = MyClass()
    my_class.ignore_cache_expiration = True # ignore cache expiration, so any existing cache file will not be deleted
    my_class.dummy("test_delete_last_saved_cache_file") # this will create a cache file if none exists
    cache_file = my_class.cache_status_dict["last_saved_cache_file"]
    os.path.exists(cache_file) # check that file exists
    deleted_cache_file = my_class.delete_last_saved_cache_file() # delete the cache file
    assert cache_file == deleted_cache_file # Check if the cache file is actually deleted
    assert not os.path.exists(cache_file) # Check if the cache file is actually deleted
    assert None == my_class.delete_last_saved_cache_file() # delete the cache file AGAIN, which should return None

