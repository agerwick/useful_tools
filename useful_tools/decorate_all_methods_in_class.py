def decorate_all(decorator): # decorator to decorate all methods in a class
    def decorate(cls):
        for attr in cls.__dict__:  # iterate over class attributes
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate
