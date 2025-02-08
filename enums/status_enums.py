from enum import Enum

class Status(Enum):
    NONE = "none"
    CALCULATED = "calculated"
    CALCULATED_APPROX = "calculated_approx"
    NEGATIVE_DISCRIMINANT = "negative_discriminant"
    ERROR = "error"