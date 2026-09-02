import json

from src.domain.entity.Beat import Beat
from src.domain.entity.Measure import Measure
from src.domain.entity.Note import Note
from src.domain.entity.Song import Song
from src.domain.enum.InstrumentTuning import InstrumentTuning
from src.domain.value_object.Duration import Duration
from src.domain.value_object.TimeSignature import TimeSignature


def section(title):
    print(f"\n{'=' * 10} {title} {'=' * 10}")


def main():
    input_path = "../tests/fixtures/example_song.json"
    output_path = "../tests/fixtures/example_song_roundtrip.json"

    # =========================================================
    # 1. Load + deserialize a full Song from JSON
    # =========================================================
    section("Loading Song from JSON")

    with open(input_path) as f:
        data = json.load(f)

    song = Song.from_dict(data)

    print(f"Loaded song: '{song.title}' by {song.artist}, {song.bpm} BPM")
    print(f"Number of tracks: {len(song.tracks)}")

    for track in song.tracks:
        print(f"\nTrack: '{track.name}' ({track.instrument.name})")
        print(f"Tuning: {track.tuning}")
        print(f"Number of measures: {len(track.measures)}")

        for i, measure in enumerate(track.measures):
            ts = measure.time_signature
            print(f"  Measure {i + 1} - time signature {ts.numerator}/{ts.denominator}")
            print(f"  Sum of durations: {measure.sum_rhythmic_events_durations()}")

            for event in measure.get_rhythmic_events():
                if hasattr(event, "notes"):
                    notes_info = [f"(string={n.string}, fret={n.fret})" for n in event.notes]
                    pitches_info = [str(track.get_pitch(n)) for n in event.notes]
                    print(f"    Beat ({event.duration.name}): {notes_info} -> {pitches_info}")
                else:
                    print(f"    Rest ({event.duration.name})")

    guitar_track = song.tracks[0]

    # =========================================================
    # 2. Tuning shifts: up_tune / down_tune / drop_tune
    # =========================================================
    section("Tuning shifts")

    # Use a separate Track for these tests - guitar_track is the same object
    # stored inside song.tracks[0], and mutating it here would affect the
    # round-trip serialization test later.
    from src.domain.entity.Track import Track
    shift_test_track = Track(name="Shift Test", measures=[], instrument=InstrumentTuning.GUITAR)

    print("Initial tuning:", shift_test_track.tuning)

    shift_test_track.down_tune()
    print("After down_tune (all strings down 1 semitone):", shift_test_track.tuning)

    shift_test_track.up_tune()
    print("After up_tune (should match initial tuning again):", shift_test_track.tuning)
    assert shift_test_track.tuning == InstrumentTuning.GUITAR.value, "up_tune did not undo down_tune correctly!"
    print("Confirmed: matches standard tuning exactly.")

    shift_test_track.drop_tune()
    print("After drop_tune (only lowest string drops a whole tone):", shift_test_track.tuning)

    # guitar_track (song.tracks[0]) was never touched, so it's still safe to use below

    # =========================================================
    # 3. Pitch + octave: crossing up and down
    # =========================================================
    section("Pitch and octave crossing")

    open_string = guitar_track.tuning[0]
    print(f"Open string 0: {open_string}")

    high_note = Note(string=0, fret=13)  # more than a full octave up
    high_pitch = guitar_track.get_pitch(high_note)
    print(f"string=0, fret=13 -> {high_pitch}")
    assert high_pitch.octave == open_string.octave + 1, "Octave did not increase when crossing upward!"
    print("Confirmed: octave increased by 1 when crossing upward.")

    # Simulate crossing an octave downward using Pitch.shift directly
    from src.domain.value_object.Pitch import Pitch
    low_pitch = Pitch.shift(open_string, -1)  # E (index 4) - 1 = D# (index 3), no crossing
    lower_pitch = Pitch.shift(open_string, -5)  # E (index 4) - 5 = -1 -> wraps to B (index 11), octave - 1
    print(f"Open string shifted by -1: {low_pitch}")
    print(f"Open string shifted by -5 (should cross down an octave): {lower_pitch}")
    assert lower_pitch.octave == open_string.octave - 1, "Octave did not decrease when crossing downward!"
    print("Confirmed: octave decreased by 1 when crossing downward.")

    # =========================================================
    # 4. Measure validation: rejecting an event that overflows
    # =========================================================
    section("Measure validation")

    test_measure = Measure(TimeSignature(4, 4))
    print("Adding QUARTER:", test_measure.add_rhythmic_event(Beat(Duration.QUARTER)))
    print("Adding QUARTER:", test_measure.add_rhythmic_event(Beat(Duration.QUARTER)))
    print("Adding HALF:", test_measure.add_rhythmic_event(Beat(Duration.HALF)))
    print("Current sum:", test_measure.sum_rhythmic_events_durations())

    overflow_result = test_measure.add_rhythmic_event(Beat(Duration.QUARTER))
    print("Adding one more QUARTER (should be rejected):", overflow_result)
    assert overflow_result is False, "Measure accepted an event that overflows the time signature!"
    print("Confirmed: overflowing event was correctly rejected.")

    # =========================================================
    # 5. Error handling: invalid data
    # =========================================================
    section("Error handling with invalid data")

    try:
        InstrumentTuning["UKULELE"]
        print("ERROR: should have raised for unknown instrument!")
    except KeyError:
        print("Confirmed: unknown instrument raises KeyError as expected.")

    try:
        Duration["EIGHTIETH"]
        print("ERROR: should have raised for unknown duration!")
    except KeyError:
        print("Confirmed: unknown duration raises KeyError as expected.")

    bad_measure_data = {
        "time_signature": {"numerator": 4, "denominator": 4},
        "rhythmic_events": [
            {"type": "GHOST", "duration": "QUARTER"}
        ]
    }
    try:
        Measure.from_dict(bad_measure_data)
        print("ERROR: should have raised for unknown rhythmic event type!")
    except ValueError as e:
        print(f"Confirmed: unknown rhythmic event type raises ValueError ({e}).")

    # =========================================================
    # 6. Save (to_dict) + round-trip comparison
    # =========================================================
    section("Serialization round-trip")

    round_trip_data = song.to_dict()

    with open(output_path, "w") as f:
        json.dump(round_trip_data, f, indent=2)

    print(f"Saved round-trip JSON to {output_path}")

    with open(output_path) as f:
        round_trip_check = json.load(f)

    matches = data == round_trip_check
    print("Round-trip matches original data:", matches)

    if not matches:
        print("Original: ", data)
        print("Round-trip:", round_trip_check)

    section("All tests completed")


if __name__ == "__main__":
    main()