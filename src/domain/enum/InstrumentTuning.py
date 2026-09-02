from enum import Enum

from src.domain.value_object.Pitch import Pitch


class InstrumentTuning(Enum):
    GUITAR = Pitch.from_name_list(["E", "B", "G", "D", "A", "E"])
    BASS = Pitch.from_name_list(["G", "D", "A", "E"])
