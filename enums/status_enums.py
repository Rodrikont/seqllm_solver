from enum import Enum

class Status(Enum):
    NONE = "none"
    CALCULATED = "calculated"
    CALCULATED_MORE_ROOTS = "calculated_more_roots"
    NEGATIVE_DISCRIMINANT = "negative_discriminant"
    ERROR = "error"