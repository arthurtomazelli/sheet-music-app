from typing import List, Optional

from src.domain.entity.Note import Note
from src.domain.entity.RhythmicEvent import RhythmicEvent
from src.domain.value_object.Duration import Duration


class Beat(RhythmicEvent):
    def __init__(self, duration: Duration, notes: Optional[List[Note]] = None) -> None:
        super().__init__(duration)
        self.notes: List[Note] = notes if notes is not None else []

    @classmethod
    def from_dict(cls, data: dict) -> "Beat":
        return cls(duration=Duration[data["duration"]], notes=[Note.from_dict(n) for n in data["notes"]])