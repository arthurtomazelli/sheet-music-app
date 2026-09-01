from typing import List

from domain.entity.Measure import Measure
from domain.entity.Note import Note
from domain.enum.InstrumentTuning import InstrumentTuning
from domain.value_object.Pitch import Pitch


class Track:
    def __init__(self, name: str, instrument: InstrumentTuning):
        self.name = name
        self.instrument = instrument
        self.tuning: List[Pitch] = instrument.value.copy()
        self.measures: List[Measure] = []

    def down_tune(self):
        self.change_tuning(-1)

    def up_tune(self):
        self.change_tuning(1)

    def change_tuning(self, shift_amount: int):
        for i, pitch in enumerate(self.tuning):
            self.tuning[i] = Pitch.shift(pitch, shift_amount)

    def drop_tune(self):
        last_string_index = len(self.tuning) - 1
        pitch = self.tuning[last_string_index]

        self.tuning[last_string_index] = Pitch.shift(pitch, -2)

    def get_pitch(self, note: Note) -> Pitch:
        open_string_pitch = self.tuning[note.string]
        return Pitch.shift(open_string_pitch, note.fret)