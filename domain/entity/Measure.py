from domain.value_object.TimeSignature import TimeSignature


class Measure:
    def __init__(self, time_signature:TimeSignature):
        self.time_signature = time_signature
        self.beats = []