# Sheet Music App

A tool to write instrument tabs (starting with guitar) and convert them to standard sheet music — and vice versa.

## Overview

The core idea is a shared internal domain model that both a tab parser and a sheet-music renderer can build on, so tab → sheet music and sheet music → tab become two rendering directions off the same data, instead of two separate conversion problems.

## Tech Stack

- **Python** — domain model, parsing engine, and API layer (single-language backend by design choice)
- **Supabase** — persistence, auth, and storage (planned)
- **Frontend** — TBD

## Project Structure

```
domain/
├── entity/
│   ├── Note.py           # A single note: string + fret (pitch is derived, not stored)
│   ├── RhythmicEvent.py  # Base class: anything that occupies a duration within a measure
│   ├── Beat.py           # RhythmicEvent: notes sounding at a given moment
│   ├── Rest.py           # RhythmicEvent: silence for a given duration
│   ├── Measure.py        # A bar: a time signature + a validated sequence of rhythmic events
│   ├── Track.py          # An instrument's part: tuning, instrument type, and its measures
│   └── Song.py           # A full piece: title, artist, bpm, and its tracks
├── enum/
│   └── InstrumentTuning.py  # Default tunings per supported instrument, as lists of Pitch
├── value_object/
│   ├── Duration.py        # Note duration, represented as a Fraction of a whole note
│   ├── TimeSignature.py   # Time signature as a NamedTuple(numerator, denominator)
│   └── Pitch.py           # A note on the chromatic scale: name + index, immutable
└── constant/
    └── chromatic_scale.py  # The 12-note chromatic scale, used internally by Pitch
```

## Current Status

The core domain model is complete and manually verified end-to-end (tuning shifts, measure validation, and the full `Song → Track → Measure → Beat/Note` chain):

- **Duration** — modeled as an `Enum` wrapping `Fraction` values, so summing durations produces musically correct results (e.g. `1/4 + 1/16 = 5/16`).
- **Pitch** — an immutable `NamedTuple` (`name`, `index`) representing a note on the chromatic scale. Only constructible through `from_name`, `from_index`, or `from_name_list`, which always compute both fields consistently — avoiding the risk of a name/index pair going out of sync. `Pitch.shift(pitch, semitones)` handles wraparound arithmetic and is the single source of truth for moving a note up or down the scale.
- **Note** — stores only `string` and `fret`. Pitch is derived from these plus the owning `Track`'s tuning, rather than stored directly.
- **RhythmicEvent** — base class for anything occupying a time slot in a measure. `Beat` (notes sounding together) and `Rest` (silence) both inherit from it, so a `Measure` can hold a single, uniformly-typed sequence of either.
- **Measure** — holds a `TimeSignature` and validates that the sum of its rhythmic events' durations never exceeds it; `add_rhythmic_event()` returns `bool` to signal acceptance/rejection, and the internal list is only accessible through `add_rhythmic_event()` (write) and `get_rhythmic_events()` (read, returns a copy).
- **Track** — one instrument's part: `name`, `InstrumentTuning`, its own mutable `tuning` (a `List[Pitch]`, copied independently from the enum default), and its `Measure`s. `up_tune()`/`down_tune()` shift every string by a semitone; `drop_tune()` shifts only the lowest string by a whole tone (e.g. standard → drop D) — all built on `Pitch.shift()`.
- **Song** — the top-level entity: `title`, `artist`, `bpm`, and its `Track`s.

## Roadmap

- [ ] Pitch calculation for a `Note` from its `string` + `fret` + the owning `Track`'s tuning
- [ ] Tab text parser → domain model
- [ ] Domain model → MusicXML / tab rendering
- [ ] Automated tests (pytest) for tuning shifts, measure validation, and pitch conversion
- [ ] FastAPI service exposing parsing/conversion
- [ ] Supabase integration (auth, persistence, storage)
- [ ] Frontend rendering (tab + standard notation)

## Design Notes

- Fret-to-pitch is deterministic (one fret position → one pitch), but pitch-to-fret is not (a pitch can usually be played at multiple fret positions) — this asymmetry is why `Note` stores string/fret rather than pitch.
- Tuning lives on `Track`, not on individual notes or beats, since it's a property of the instrument's setup for the whole piece, not something that varies beat-to-beat.
- The chromatic scale is a plain module-level constant (not a class or enum), since it's used purely as an ordered, indexable sequence internal to `Pitch` — no other class references it directly.
- `Pitch` restricts construction to its classmethods rather than allowing `name` and `index` to be passed independently, since the two must always agree; Python can't truly enforce this (no private constructors), so it relies on convention rather than a hard guarantee.
- Encapsulation (protected attribute + accessor methods) is applied only where a real invariant is being protected — `Measure._rhythmic_events`, since it must never exceed the time signature. Simpler collections (`Beat.notes`, `Track.measures`, `Song.tracks`) are left as plain public lists, since Python idiom avoids getters/setters without a concrete reason.
