def get_first(collection, filter_func):
    for i in collection:
        if filter_func(i):
            return i

    return None
