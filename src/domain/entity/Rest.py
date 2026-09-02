from src.domain.entity.RhythmicEvent import RhythmicEvent
from src.domain.enum.RhythmicEventType import RhythmicEventType
from src.domain.value_object.Duration import Duration


class Rest(RhythmicEvent):
    def __init__(self, duration: Duration):
        super().__init__(duration)

    @classmethod
    def from_dict(cls, data: dict) -> "Rest":
        return cls(duration=Duration[data["duration"]])

    def to_dict(self) -> dict:
        return {"duration": self.duration.name, "type": RhythmicEventType.REST.name}