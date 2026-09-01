# Sheet Music App

A tool to write instrument tabs (starting with guitar) and convert them to standard sheet music — and vice versa.

## Overview

The core idea is a shared internal domain model that both a tab parser and a sheet-music renderer can build on, so tab → sheet music and sheet music → tab become two rendering directions off the same data, instead of two separate conversion problems.

## Tech Stack

- **Python** — domain model, parsing engine, and API layer (single-language backend by design choice)
- **Supabase** — persistence, auth, and storage (planned)
- **Frontend** — TBD

## Roadmap

- [ ] Pitch calculation from `Note` (string + fret + `Track.tuning`)
- [ ] Tab text parser → domain model
- [ ] Domain model → MusicXML / tab rendering
- [ ] FastAPI service exposing parsing/conversion
- [ ] Supabase integration (auth, persistence, storage)
- [ ] Frontend rendering (tab + standard notation)

## Design Notes

- Fret-to-pitch is deterministic (one fret position → one pitch), but pitch-to-fret is not (a pitch can usually be played at multiple fret positions) — this asymmetry is why `Note` stores string/fret rather than pitch.
- Tuning lives on `Track`, not on individual notes or beats, since it's a property of the instrument's setup for the whole piece, not something that varies beat-to-beat.
- The chromatic scale is a plain module-level constant (not a class or enum), since it's used purely as an ordered, indexable sequence, not accessed by individual named members.