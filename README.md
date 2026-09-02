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
│   ├── RhythmicEvent.py  # Abstract base class: anything that occupies a duration within a measure
│   ├── Beat.py           # RhythmicEvent: notes sounding at a given moment
│   ├── Rest.py           # RhythmicEvent: silence for a given duration
│   ├── Measure.py        # A bar: a time signature + a validated sequence of rhythmic events
│   ├── Track.py          # An instrument's part: tuning, instrument type, and its measures
│   └── Song.py           # A full piece: title, artist, bpm, and its tracks
├── enum/
│   ├── InstrumentTuning.py   # Default tunings per supported instrument, as lists of Pitch
│   └── RhythmicEventType.py  # BEAT / REST discriminator used in JSON serialization
├── value_object/
│   ├── Duration.py        # Note duration, represented as a Fraction of a whole note
│   ├── TimeSignature.py   # Time signature as a NamedTuple(numerator, denominator)
│   └── Pitch.py           # A note on the chromatic scale: name + index, immutable
└── constant/
    └── chromatic_scale.py  # The 12-note chromatic scale, used internally by Pitch
tests/
└── fixtures/
    └── example_song.json  # Sample song exercising standard + custom tuning, beats, rests, chords
```

## Current Status

The core domain model is complete, including pitch resolution and full JSON serialization, all manually verified end-to-end (tuning shifts, measure validation, pitch calculation, and a load → deserialize → serialize → save round-trip that matches the original data exactly):

- **Duration** — modeled as an `Enum` wrapping `Fraction` values, so summing durations produces musically correct results (e.g. `1/4 + 1/16 = 5/16`).
- **Pitch** — an immutable `NamedTuple` (`name`, `index`, `octave`) representing a specific note on the chromatic scale, at a specific octave. Only constructible through `from_name`, `from_index`, or `from_name_list`, which always compute `index` from `name` consistently — avoiding the risk of a name/index pair going out of sync. `octave` is always required explicitly (never guessed), since it can't be derived from a note name alone. `Pitch.shift(pitch, semitones)` handles wraparound arithmetic in both directions — using floor division on the pre-modulo index sum to correctly track octave crossings — and is the single source of truth for moving a note up or down the scale, used identically by fret-based pitch lookups and by tuning changes.
- **Note** — stores only `string` and `fret`. Pitch is resolved on demand via `Track.get_pitch(note)`, which looks up the open-string `Pitch` for that string and applies the fret offset through `Pitch.shift()` — nothing is stored redundantly on `Note` itself.
- **RhythmicEvent** — now an abstract base class (`ABC`), guaranteeing every subclass implements `to_dict()`. `Beat` (notes sounding together) and `Rest` (silence) both inherit from it, so a `Measure` can hold a single, uniformly-typed sequence of either.
- **Measure** — holds a `TimeSignature` and validates that the sum of its rhythmic events' durations never exceeds it; `add_rhythmic_event()` returns `bool` to signal acceptance/rejection, and the internal list is only accessible through `add_rhythmic_event()` (write) and `get_rhythmic_events()` (read, returns a copy). This validation runs the same way whether a `Measure` is built manually or from JSON.
- **Track** — one instrument's part: `name`, `InstrumentTuning`, its own mutable `tuning` (a `List[Pitch]`, copied independently from the enum default), and its `Measure`s. `up_tune()`/`down_tune()` shift every string by a semitone; `drop_tune()` shifts only the lowest string by a whole tone (e.g. standard → drop D) — all built on `Pitch.shift()`. `get_pitch(note)` resolves a note's actual pitch using the track's current tuning.
- **Song** — the top-level entity: `title`, `artist`, `bpm`, and its `Track`s.
- **JSON serialization** — every entity and value object has matching `from_dict`/`to_dict` methods, letting a full `Song` be loaded from and saved back to JSON. `RhythmicEventType` (`BEAT`/`REST`) replaces hardcoded strings as the type discriminator. A `Track`'s `tuning` is only written to JSON when it differs from the instrument's default, avoiding redundant data for the common case.

## Roadmap

- [ ] Automated tests (pytest) for tuning shifts, measure validation, pitch conversion, and JSON round-tripping
- [ ] Domain model → MusicXML / tab rendering
- [ ] FastAPI service exposing parsing/conversion (structured JSON in/out — matches how the frontend will create tabs)
- [ ] Supabase integration (auth, persistence, storage)
- [ ] Frontend rendering (tab + standard notation)
- [ ] ASCII tab text parser → domain model (deferred: needed only for importing existing tabs from external sources; the frontend's own tab-creation flow already produces structured JSON directly, no text parsing involved)

## Design Notes

- Fret-to-pitch is deterministic (one fret position → one pitch), but pitch-to-fret is not (a pitch can usually be played at multiple fret positions) — this asymmetry is why `Note` stores string/fret rather than pitch.
- Tuning lives on `Track`, not on individual notes or beats, since it's a property of the instrument's setup for the whole piece, not something that varies beat-to-beat.
- `Track.get_pitch(note)` lives on `Track` rather than `Note` or `Pitch`, since `Track` is the only place where both required inputs — tuning and note position — naturally meet, without making `Note`/`Pitch` aware of concepts outside themselves.
- The chromatic scale is a plain module-level constant (not a class or enum), since it's used purely as an ordered, indexable sequence internal to `Pitch` — no other class references it directly.
- `Pitch` restricts construction to its classmethods rather than allowing `name` and `index` to be passed independently, since the two must always agree; Python can't truly enforce this (no private constructors), so it relies on convention rather than a hard guarantee.
- Encapsulation (protected attribute + accessor methods) is applied only where a real invariant is being protected — `Measure._rhythmic_events`, since it must never exceed the time signature. Simpler collections (`Beat.notes`, `Track.measures`, `Song.tracks`) are left as plain public lists, since Python idiom avoids getters/setters without a concrete reason.
- All `from_dict`/`to_dict` methods use keyword arguments when constructing objects, to avoid silent bugs if a constructor's parameter order ever changes.
- `to_dict()` on `RhythmicEvent` subclasses relies on polymorphism (`event.to_dict()`) rather than `isinstance` checks; making `RhythmicEvent` abstract ensures any future subclass is forced to implement it.
