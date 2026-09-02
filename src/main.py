import json

from src.domain.entity.Song import Song


def main():
    input_path = "../tests/fixtures/example_song.json"
    output_path = "../tests/fixtures/example_song_roundtrip.json"

    # --- Load (from_dict) ---
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
            print(f"  Measure {i + 1} - time signature {measure.time_signature.numerator}/{measure.time_signature.denominator}")
            print(f"  Sum of durations: {measure.sum_rhythmic_events_durations()}")

            for event in measure.get_rhythmic_events():
                if hasattr(event, "notes"):
                    notes_info = [f"(string={n.string}, fret={n.fret})" for n in event.notes]
                    pitches_info = [str(track.get_pitch(n)) for n in event.notes]
                    print(f"    Beat ({event.duration.name}): {notes_info} -> {pitches_info}")
                else:
                    print(f"    Rest ({event.duration.name})")

    # --- Save (to_dict) ---
    round_trip_data = song.to_dict()

    with open(output_path, "w") as f:
        json.dump(round_trip_data, f, indent=2)

    print(f"\nSaved round-trip JSON to {output_path}")

    # --- Compare original vs round-trip ---
    with open(output_path) as f:
        round_trip_check = json.load(f)

    print("Round-trip matches original data:", data == round_trip_check)

    if data != round_trip_check:
        print("Original: ", data)
        print("Round-trip:", round_trip_check)


if __name__ == "__main__":
    main()