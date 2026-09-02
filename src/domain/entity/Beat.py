from typing import List

from src.domain.entity.Note import Note
from src.domain.entity.RhythmicEvent import RhythmicEvent
from src.domain.value_object.Duration import Duration


class Beat(RhythmicEvent):
    def __init__(self, duration: Duration):
        super().__init__(duration)
        self.notes: List[Note] = []
