import re
import urllib.request
import urllib.parse
from enum import Enum

# TODO currently only matches last occurrence
__REGEX_CONVERTER__ = re.compile(r'.*(<(string|int|float):(\w+)>)+.*', re.IGNORECASE)


def make_url(base_url: str, **kwargs):
    """
    Make a url
    :param base_url:    base url
    :param kwargs:      key/value pairs for parameters and arguments
    :return:
    """
    url = base_url
    args = kwargs
    match = __REGEX_CONVERTER__.match(base_url)
    if match:
        if match.group(3) in kwargs.keys():
            url = url.replace(match.group(1), str(kwargs.get(match.group(3))))
            args = {k: v for k, v in kwargs.items() if k != match.group(3)}

    params = urllib.parse.urlencode(args)
    return f'{url}?{params}' if args is not None and len(args) > 0 else url


class MatchParam(Enum):
    IGNORE = 1              # don't try to match

    # EXACT = 2               # match exactly
    # CONTAINS = 3            # match contains
    CASE_SENSITIVE = 4      # case sensitive match
    CASE_INSENSITIVE = 5    # case insensitive match
    TRUE = 6                # match true
    FALSE = 7               # match false
    EQUAL = 8               # match equal
    NOT_EQUAL = 9           # match not equal
    IN = 10                 # match expected in value

    TO_INT = 50             # convert to int

    def __eq__(self, other):
        if self.__class__.__name__ == other.__class__.__name__ and isinstance(other, Enum):
            return self.value == other.value
        return NotImplemented


class Expect(Enum):
    SUCCESS = 1
    FAILURE = 2

