from fractions import Fraction
from typing import List, Optional, Final

from src.domain.entity.Beat import Beat
from src.domain.entity.Rest import Rest
from src.domain.entity.RhythmicEvent import RhythmicEvent
from src.domain.enum.RhythmicEventType import RhythmicEventType
from src.domain.value_object.TimeSignature import TimeSignature


class Measure:
    ZERO_VALUE_FRACTION: Final = Fraction(0, 1)

    def __init__(self, time_signature: TimeSignature):
        self.time_signature = time_signature
        self._rhythmic_events: List[RhythmicEvent] = []

    def add_rhythmic_event(self, event: RhythmicEvent) -> bool:
        time_signature_value = Fraction(self.time_signature.numerator, self.time_signature.denominator)

        if self.sum_rhythmic_events_durations(event) <= time_signature_value:
            self._rhythmic_events.append(event)

            return True

        return False

    def sum_rhythmic_events_durations(self, event: Optional[RhythmicEvent] = None) -> Fraction:
        duration_sum = self.ZERO_VALUE_FRACTION

        for rhythmic_event in self._rhythmic_events:
            duration_sum += rhythmic_event.duration.value

        duration_sum += event.duration.value if event else self.ZERO_VALUE_FRACTION

        return duration_sum

    @classmethod
    def from_dict(cls, data: dict) -> "Measure":
        measure: Measure = cls(time_signature=TimeSignature.from_dict(data["time_signature"]))

        for rhythmic_event in data["rhythmic_events"]:
            if rhythmic_event["type"] == RhythmicEventType.BEAT.name:
                measure.add_rhythmic_event(Beat.from_dict(rhythmic_event))
            elif rhythmic_event["type"] == RhythmicEventType.REST.name:
                measure.add_rhythmic_event(Rest.from_dict(rhythmic_event))
            else:
                raise ValueError("Unknown rhythmic event type")

        return measure

    def to_dict(self) -> dict:
        return {
            "time_signature": self.time_signature.to_dict(),
            "rhythmic_events": [rhythmic_event.to_dict() for rhythmic_event in self._rhythmic_events],
        }

    def get_rhythmic_events(self) -> List[RhythmicEvent]:
        return self._rhythmic_events.copy()