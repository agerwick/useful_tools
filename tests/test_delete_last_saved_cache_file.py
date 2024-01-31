import os
from useful_tools.cache_decorators import delete_last_saved_cache_file

class MyClass:
    def __init__(self):
        self.last_saved_cache_file = "cache_file.txt"

    @delete_last_saved_cache_file
    def delete_cache(self):
        pass # pragma: no cover

class MyIncorrectlySetUpClass:
    @delete_last_saved_cache_file
    def delete_cache(self):
        pass # pragma: no cover

def test_delete_last_saved_cache_file():
    my_class = MyClass()
    cache_file = "my_dummy_cache_file.txt"
    my_class.last_saved_cache_file = cache_file

    # Create a dummy cache file
    with open(cache_file, "w") as file:
        file.write("dummy cache data")

    # check that file exists
    assert os.path.exists(cache_file)

    # Call the delete_cache method
    assert cache_file == my_class.delete_cache()

    # Check if the cache file is deleted
    assert not os.path.exists(cache_file)

def test_delete_last_saved_cache_file_with_non_existent_file():
    my_class = MyClass()
    cache_file = "non-existing_file.txt"
    my_class.last_saved_cache_file = cache_file

    # check that file does not exist
    assert not os.path.exists(cache_file)

    # Call the delete_cache method
    assert None == my_class.delete_cache()

    # Check if the cache file is deleted
    assert not os.path.exists(cache_file)

def test_delete_last_saved_cache_file_with_non_existent_attribute():
    my_class = MyIncorrectlySetUpClass()

    # check that file does not exist
    assert not hasattr(my_class, "last_saved_cache_file")

    # Call the delete_cache method and check that it does not raise an exception
    assert None == my_class.delete_cache()
