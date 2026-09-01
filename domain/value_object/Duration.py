from enum import Enum
from fractions import Fraction

class Duration(Enum):
    WHOLE = Fraction(1, 1)
    HALF = Fraction(1, 2)
    QUARTER = Fraction(1, 4)
    EIGHTH = Fraction(1, 8)
    SIXTEENTH = Fraction(1, 16)