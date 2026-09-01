from typing import List

from domain.entity.Measure import Measure
from domain.enum.InstrumentTuning import InstrumentTuning
from domain.constant.CHROMATIC_SCALE import chromatic_scale


class Track:
    def __init__(self, name: str, instrument: InstrumentTuning):
        self.name = name
        self.instrument = instrument
        self.tuning: List[str] = instrument.value.copy()
        self.measures: List[Measure] = []

    def down_tune(self):
        self.change_tuning(-1)

    def up_tune(self):
        self.change_tuning(1)

    def change_tuning(self, change: int):
        for i, note in enumerate(self.tuning):
            self.shift_note(i, note, change)

    def drop_tune(self):
        last_string_index = len(self.tuning) - 1
        note = self.tuning[last_string_index]

        self.shift_note(last_string_index, note, -2)

    def shift_note(self, index: int, note: str, shift: int):
        self.tuning[index] = chromatic_scale[(chromatic_scale.index(note) + shift) % 12]
