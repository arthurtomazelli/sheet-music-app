from typing import List

from src.domain.entity.Track import Track


class Song:
    def __init__(self, title: str, artist: str, bpm: int, tracks: List[Track]):
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.tracks: List[Track] = tracks

    @classmethod
    def from_dict(cls, data: dict) -> "Song":
        return cls(title=data["title"],
                   artist=data["artist"],
                   bpm=data["bpm"],
                   tracks=[Track.from_dict(t) for t in data["tracks"]]
        )
