from enum import Enum


class QueryParam(Enum):
    GET_FIRST = 1
    GET_ALL = 2
    COUNT = 3

    UPDATE_SET = 4  # Set values during an update.
    UPDATE_ADD = 5  # Add to existing values during an update.

    def __eq__(self, other):
        if self.__class__.__name__ == other.__class__.__name__ and isinstance(other, Enum):
            return self.value == other.value
        return NotImplemented
