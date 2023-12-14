from collections import OrderedDict
from itertools import chain


def order_and_flatten_obj(obj):
    if isinstance(obj, dict):
        return dict(OrderedDict(sorted((k, order_and_flatten_obj(v)) for k, v in obj.items())))
    if type(obj) in [list, set]:
        return type(obj)(chain.from_iterable(order_and_flatten_obj(x) for x in obj))
    else:
        return obj


def is_equal_dict(dict1, dict2):
    """
    Recursively checks if 2 dictionaries are equal in content, regardless of order of keys/nested elements.

    """
    return order_and_flatten_obj(dict1) == order_and_flatten_obj(dict2)
