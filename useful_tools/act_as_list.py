def act_as_list(attribute):
    """
This class decorator adds list-like behavior to a class.

What's the point?
- you can add methods to the class, which you can't do with a list
- compared to adding the list-like methods you need directly on the class, 
    it makes the class look neater, keeping it DRY, so it's easier to read
- also, you should not inherit from list 
    (as it's implemented in C, so it could have unintended consequences)
    so this is the best solution I could come up with
- the result is that objects of classes with this decorator look and act like a list

Usage example:
```
@act_as_list('servers_list')
class Servers:
    def __init__(self, servers_list):
        self.servers_list = servers_list
    def status_report(self):
        # return a dict of server: status
        return {server: self.get_status(server) for server in self.servers_list}
    @classmethod
    def get_status(cls, server):
        # return the status of a server
        return "online" # or "offline"
# instead of servers.server_list, you can just use servers, as if it was a list
servers = Servers(["server1", "server2"])
print(servers.servers_list) # prints ['server1', 'server2']
print(servers) # prints ['server1', 'server2']
len(servers) # prints 2
for server in servers: # iterates over the list
    print(server) # prints 'server1' and 'server2'
# and this is where it differs from a list:
servers.status_report() # returns {'server1': 'online', 'server2': 'online'}
```

Usage example 2:
```
@act_as_list('objects')
class MyClassThatLooksLikeAList:
    def __init__(self, objects = []):
        self.objects = objects
    def in_uppercase(self):
        return " ".join(self).upper()
    def contains_both_hello_and_world(self):
        return "hello" in self and "world" in self

fake_list = MyClassThatLooksLikeAList()
fake_list.append("hello")
fake_list.append("world")
print(fake_list.objects) # prints ['hello', 'world']
print(fake_list) # prints ['hello', 'world']
print(fake_list[0]) # prints 'hello'
print(fake_list.index("world")) # prints 1
print(len(fake_list)) # prints 2
print(list(reversed(fake_list))) # prints ['world', 'hello']
print(fake_list.pop()) # prints 'world'
print(fake_list.contains_both_hello_and_world()) # prints False
fake_list = MyClassThatLooksLikeAList(["hello", "world"])
print(fake_list.contains_both_hello_and_world()) # prints True
print(fake_list.in_uppercase()) # prints "HELLO WORLD"
```
    """
    def decorator(cls):
        class ActsLikeAList(cls):
            def __eq__(self, other):
                """for comparison with other lists: myfakelist == ["hello", "world"] """
                return list(getattr(self, attribute)) == other
            
            def __getitem__(self, index):
                """for getting an item by index: myfakelist[0]"""
                return getattr(self, attribute)[index]

            def __setitem__(self, index, value):
                """for setting an item by index: myfakelist[0] = "hello" """
                getattr(self, attribute)[index] = value
            
            def __len__(self):
                """for getting the length of the list: len(myfakelist)"""
                return len(getattr(self, attribute))

            def __iter__(self):
                """for iterating over the list: for item in myfakelist:
                (although this is also made possible by __getitem__)"""
                return iter(getattr(self, attribute))

            def __contains__(self, item):
                """for checking if an item is in the list: "hello" in myfakelist"""
                return item in getattr(self, attribute)

            def __add__(self, other):
                """for adding two lists: myfakelist + ["hello", "world"] """
                if isinstance(other, list):
                    other = self.__class__(other) # convert to the same class as self
                return self.__class__(getattr(self, attribute) + getattr(other, attribute))

            def __str__(self):
                """for printing the list: print(myfakelist)"""
                return str(getattr(self, attribute))

            def __repr__(self):
                """for printing the list with the class name: myfakelist"""
                return f"{self.__class__.__name__}({getattr(self, attribute)})"
            
            def __reversed__(self):
                """for reversing the list: reversed(myfakelist)"""
                return reversed(getattr(self, attribute))

            def reverse(self):
                """for reversing the list: myfakelist.reverse()"""
                getattr(self, attribute).reverse()

            def append(self, item):
                """for appending an item to the list: myfakelist.append("hello")"""
                getattr(self, attribute).append(item)

            def insert(self, index, item):
                """for inserting an item at a specific index: myfakelist.insert(0, "hello")"""
                getattr(self, attribute).insert(index, item)

            def count(self, item):
                """for counting the number of times an item occurs in the list: myfakelist.count("hello")"""
                return getattr(self, attribute).count(item)
            
            def extend(self, iterable):
                """for extending the list with another iterable: myfakelist.extend(["hello", "world"])"""
                getattr(self, attribute).extend(iterable)

            def clear(self):
                """for clearing the list: myfakelist.clear()"""
                getattr(self, attribute).clear()

            def copy(self):
                """for copying the list: myfakelist.copy()"""
                return getattr(self, attribute).copy()
            
            def index(self, item):
                """for getting the index of an item in the list: myfakelist.index("hello")"""
                return getattr(self, attribute).index(item)
            
            def pop(self, index = -1):
                """for popping an item from the list: myfakelist.pop()"""
                return getattr(self, attribute).pop(index)
            
            def remove(self, item):
                """for removing an item from the list: myfakelist.remove("hello")"""
                getattr(self, attribute).remove(item)

            def sort(self, *args, **kwargs):
                """for sorting the list: myfakelist.sort()"""
                getattr(self, attribute).sort(*args, **kwargs)

        # assign the name and qualname of the original class to the new class
        # otherwise, the name of the class will be 'ActsLikeAList'
        ActsLikeAList.__name__ = cls.__name__
        ActsLikeAList.__qualname__ = cls.__qualname__
        return ActsLikeAList
    return decorator
