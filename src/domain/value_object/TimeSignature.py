from typing import NamedTuple


class TimeSignature(NamedTuple):
    numerator: int
    denominator: int

    @classmethod
    def from_dict(cls, data: dict) -> "TimeSignature":
        return cls(numerator=data["numerator"], denominator=data["denominator"])

    def to_dict(self) -> dict:
        return {"numerator": self.numerator, "denominator": self.denominator}