class Note:
    def __init__(self, string: int, fret: int):
        self.string = string
        self.fret = fret

    @classmethod
    def from_dict(cls, data: dict ) -> "Note":
        return cls(string=data["string"], fret=data["fret"])