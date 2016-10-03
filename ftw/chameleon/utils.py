

def get_subclasses(cls):
    yield cls
    for classes in map(get_subclasses, cls.__subclasses__()):
        for subclass in classes:
            yield subclass
