from typing import List

from domain.entity.Note import Note
from domain.entity.RhythmicEvent import RhythmicEvent
from domain.value_object.Duration import Duration


class Beat(RhythmicEvent):
    def __init__(self, duration: Duration):
        super().__init__(duration)
        self.notes: List[Note] = []
