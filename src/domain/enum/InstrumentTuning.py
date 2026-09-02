from enum import Enum

from src.domain.value_object.Pitch import Pitch


class InstrumentTuning(Enum):
    GUITAR = Pitch.from_name_list([("E", 4), ("B", 3), ("G", 3), ("D", 3), ("A", 2), ("E", 2)])
    BASS = Pitch.from_name_list([("G", 2), ("D", 2), ("A", 1), ("E", 1)])
