from domain.entity.RhythmicEvent import RhythmicEvent
from domain.value_object.Duration import Duration


class Rest(RhythmicEvent):
    def __init__(self, duration: Duration):
        super().__init__(duration)