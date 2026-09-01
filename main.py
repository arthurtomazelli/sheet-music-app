from domain.entity.Beat import Beat
from domain.entity.Measure import Measure
from domain.entity.Note import Note
from domain.entity.Song import Song
from domain.entity.Track import Track
from domain.enum.InstrumentTuning import InstrumentTuning
from domain.value_object.Duration import Duration
from domain.value_object.TimeSignature import TimeSignature


def main():
    # --- Test Track + Pitch tuning shifts ---
    guitar_track = Track("My Track", InstrumentTuning.GUITAR)
    print("Initial tuning:", guitar_track.tuning)

    # down_tune shifts ALL strings by one semitone
    guitar_track.down_tune()
    print("After down_tune (all strings shift):", guitar_track.tuning)

    guitar_track.up_tune()
    print("After up_tune (should match initial tuning again):", guitar_track.tuning)

    # drop_tune only shifts the lowest string, by 2 semitones (e.g. standard -> drop D)
    guitar_track.drop_tune()
    print("After drop_tune (only lowest string shifts):", guitar_track.tuning)

    # --- Test Measure + Beat + validation ---
    measure = Measure(TimeSignature(4, 4))

    beat1 = Beat(Duration.QUARTER)
    beat1.notes.append(Note(string=0, fret=0))

    beat2 = Beat(Duration.QUARTER)
    beat2.notes.append(Note(string=1, fret=2))

    beat3 = Beat(Duration.HALF)
    beat3.notes.append(Note(string=2, fret=3))

    print("\nAdding beats to a 4/4 measure:")
    print("Added beat1 (1/4):", measure.add_rhythmic_event(beat1))
    print("Added beat2 (1/4):", measure.add_rhythmic_event(beat2))
    print("Added beat3 (1/2):", measure.add_rhythmic_event(beat3))
    print("Current sum:", measure.sum_rhythmic_events_durations())

    # This one should be rejected — measure is already full (4/4 = 1)
    extra_beat = Beat(Duration.QUARTER)
    print("Trying to add one more (should be False):", measure.add_rhythmic_event(extra_beat))

    # --- Test Song + Track relationship ---
    song = Song("Wonderwall", "Oasis", 87)
    song.tracks.append(guitar_track)
    guitar_track.measures.append(measure)

    print(f"\nSong '{song.title}' by {song.artist} at {song.bpm} BPM")
    print(f"Track '{guitar_track.name}' has {len(guitar_track.measures)} measure(s)")
    print(f"That measure has {len(measure._rhythmic_events)} rhythmic event(s)")


if __name__ == "__main__":
    main()