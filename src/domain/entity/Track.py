from typing import List, Optional

from src.domain.entity.Measure import Measure
from src.domain.entity.Note import Note
from src.domain.enum.InstrumentTuning import InstrumentTuning
from src.domain.value_object.Pitch import Pitch


class Track:
    def __init__(self, name: str,
                 measures: List[Measure],
                 instrument: InstrumentTuning,
                 tuning: Optional[List[Pitch]] = None):
        self.name = name
        self.instrument = instrument
        self.tuning: List[Pitch] = tuning if tuning is not None else instrument.value.copy()
        self.measures: List[Measure] = measures

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

    @classmethod
    def from_dict(cls, data: dict) -> "Track":
        return cls(name=data["name"],
                   measures=[Measure.from_dict(m) for m in data["measures"]],
                   instrument=InstrumentTuning[data["instrument"]],
                   tuning=[Pitch.from_dict(pitch_dict) for pitch_dict in data["tuning"]] if "tuning" in data else None
        )

    def to_dict(self) -> dict:
        data: dict = {
            "name": self.name,
            "measures": [measure.to_dict() for measure in self.measures],
            "instrument": self.instrument.name,
        }

        if self.tuning != self.instrument.value:
            data["tuning"] = [pitch.to_dict() for pitch in self.tuning]

        return data