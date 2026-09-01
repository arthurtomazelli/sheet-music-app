from domain.value_object.Duration import Duration


class RhythmicEvent:
    def __init__(self, duration: Duration):
        self.duration = duration