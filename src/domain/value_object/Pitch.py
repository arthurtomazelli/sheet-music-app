from typing import NamedTuple, List, Tuple

from src.domain.constant.CHROMATIC_SCALE import chromatic_scale


class Pitch(NamedTuple):
    name: str
    index: int
    octave: int

    @classmethod
    def from_name(cls, name: str, octave: int) -> "Pitch":
        return cls(name, chromatic_scale.index(name), octave)

    @classmethod
    def from_index(cls, index: int, octave: int) -> "Pitch":
        return cls(chromatic_scale[index], index, octave)

    @staticmethod
    def from_name_list(name_list: List[Tuple[str, int]]) -> List["Pitch"]:
        return [Pitch.from_name(name, octave) for name, octave in name_list]

    @staticmethod
    def shift(pitch: "Pitch", shift_amount: int) -> "Pitch":
        new_octave = pitch.octave + (pitch.index + shift_amount) // 12
        return Pitch.from_index((pitch.index + shift_amount)% 12, new_octave)

    @classmethod
    def from_dict(cls, data: dict) -> "Pitch":
        return Pitch.from_name(name=data["name"], octave=data["octave"])

    def to_dict(self) -> dict:
        return {"name": self.name, "octave": self.octave}