from fractions import Fraction
from typing import List, Optional

from domain.entity.RhythmicEvent import RhythmicEvent
from domain.value_object.TimeSignature import TimeSignature


class Measure:
    def __init__(self, time_signature: TimeSignature):
        self.time_signature = time_signature
        self.rhythmic_events: List[RhythmicEvent] = []

    def add_rhythmic_event(self, event: RhythmicEvent):
        time_signature_value = Fraction(self.time_signature.numerator, self.time_signature.denominator)

        if self.sum_rhythmic_events_durations(event) <= time_signature_value:
            self.rhythmic_events.append(event)

    def sum_rhythmic_events_durations(self, event: Optional[RhythmicEvent] = None):
        duration_sum = 0

        for rhythmic_event in self.rhythmic_events:
            duration_sum += rhythmic_event.duration.value

        duration_sum += event.duration.value if event else 0

        return duration_sum
