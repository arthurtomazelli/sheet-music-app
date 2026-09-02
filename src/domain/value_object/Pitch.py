from typing import NamedTuple, List

from src.domain.constant.CHROMATIC_SCALE import chromatic_scale


class Pitch(NamedTuple):
    name: str
    index: int

    @classmethod
    def from_name(cls, name: str) -> "Pitch":
        return cls(name, chromatic_scale.index(name))

    @classmethod
    def from_index(cls, index: int) -> "Pitch":
        return cls(chromatic_scale[index], index)

    @staticmethod
    def from_name_list(name_list: List[str]) -> List["Pitch"]:
        return [Pitch.from_name(name) for name in name_list]

    @staticmethod
    def shift(pitch: "Pitch", shift_amount: int) -> "Pitch":
        return Pitch.from_index((pitch.index + shift_amount)% 12)