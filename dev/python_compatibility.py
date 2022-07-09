import sys

PY2 = sys.version_info[0] == 2


def is_string(obj):
    if PY2:
        # noinspection PyUnresolvedReferences
        return isinstance(obj, basestring)

    return isinstance(obj, str)