from abc import abstractmethod, ABC

from src.domain.value_object.Duration import Duration


class RhythmicEvent(ABC):
    def __init__(self, duration: Duration):
        self.duration = duration

    @abstractmethod
    def to_dict(self) -> dict:
        pass