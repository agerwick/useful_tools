import hashlib

def make_hashable(obj):
    """make an object hashable, so it can be used as an identifier for the cache"""
    # recursively convert lists and dicts to tuples and frozensets
    if isinstance(obj, (tuple, list)):
        # the order og args is relevant, so the order of the items in the tuple should not be changed
        return tuple(make_hashable(e) for e in obj)
    elif isinstance(obj, dict):
        # sort the dict by key before converting to frozenset, as the order of kwargs (and keys in a dict) is not relevant, so the order of the keys should not affect the hash
        return frozenset((k, make_hashable(v)) for k, v in sorted(obj.items()))
    return obj

def make_arg_hash(args, kwargs):
    """make a hash of the arguments that can be used to check if the arguments are the same as something that was previously cached"""
    # preserve the order or args, so calling a function with the same arguments in a different order will NOT give the same hash
    # this is important for the cache, because the cache should not be used if the arguments are different
    # frozenset is used because it makes the args hashable
    # the arguments are put in a list of one item before being converted to a frozenset to preserve the order of the arguments
    hashable_args = make_hashable([args])
    hashable_kwargs = make_hashable(kwargs)
    encoded_arg_str = f"{hashable_args}_{hashable_kwargs}".encode()
    sha256hash = hashlib.sha256(encoded_arg_str).hexdigest()
    return sha256hash
