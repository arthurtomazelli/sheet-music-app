from typing import List

from src.domain.entity.Track import Track


class Song:
    def __init__(self, title: str, artist: str, bpm: int):
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.tracks: List[Track] = []
