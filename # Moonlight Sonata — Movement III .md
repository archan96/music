# Moonlight Sonata — Movement III (Presto agitato)
Converted from your uploaded MusicXML (`moonlight_sonata_3rd_movement.mxl`).

**Composer:** Ludwig van Beethoven  
**Movement:** III (as you said)  
**Key signature:** 4 sharps → rendered as **C# minor** in ABC header  
**Time:** 4/4  
**Tempo (from file):** ♩ = 170.0

---

## Files generated

- `moonlight_sonata_movement3_simplified.abc` — **recommended** (RH + LH5 + LH6)
- `moonlight_sonata_movement3_allvoices.abc` — **lossless** (all 6 voices found in the MusicXML)
- `moonlight_sonata_movement3_events.csv` — every note/rest as a table (measure, staff, voice, start, duration, pitches)

---

## How to read the pitches

### Scientific pitch (table)
Examples: `C#4`, `G#3`, `E5` (octave numbers: **C4 = middle C**)

### ABC pitch (ABC files)
- `C` = C4 (middle C), `c` = C5  
- `C,` = C3, `C,,` = C2  
- `^` = sharp (so `^G` = G#), `_` = flat

Durations assume `L:1/16`:
- no number = 1/16 note
- `2` = 1/8, `4` = 1/4, `8` = 1/2, `16` = whole note
- fractions like `1/2` indicate shorter-than-1/16 values (e.g., 1/32)

---

## Quick event preview (first ~40 events)

| measure | staff | voice | start_beats_frac | duration_beats_frac | pitches_scientific | abc_token |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 2 | REST | z8 |
| 1 | 1 | 1 | 2 | 1 | REST | z4 |
| 1 | 1 | 1 | 3 | 1/4 | E4 | E |
| 1 | 1 | 1 | 13/4 | 1/4 | G#3 | ^G, |
| 1 | 1 | 1 | 7/2 | 1/4 | C#4 | ^C |
| 1 | 1 | 1 | 15/4 | 1/4 | E4 | E |
| 1 | 1 | 6 | 11/4 | 1/4 | C#4 | ^C |
| 1 | 2 | 5 | 0 | 1/2 | C#2 | ^C,,2 |
| 1 | 2 | 5 | 1/2 | 1/2 | G#2 | ^G,,2 |
| 1 | 2 | 5 | 1 | 1/2 | C#2 | ^C,,2 |
| 1 | 2 | 5 | 3/2 | 1/2 | G#2 | ^G,,2 |
| 1 | 2 | 5 | 2 | 1/2 | C#2 | ^C,,2 |
| 1 | 2 | 5 | 5/2 | 1/2 | G#2 | ^G,,2 |
| 1 | 2 | 5 | 3 | 1/2 | C#2 | ^C,,2 |
| 1 | 2 | 5 | 7/2 | 1/2 | G#2 | ^G,,2 |
| 1 | 2 | 6 | 0 | 1/4 | REST | z |
| 1 | 2 | 6 | 1/4 | 1/4 | G#2 | ^G,, |
| 1 | 2 | 6 | 1/2 | 1/4 | C#3 | ^C, |
| 1 | 2 | 6 | 3/4 | 1/4 | E3 | E, |
| 1 | 2 | 6 | 1 | 1/4 | G#3 | ^G, |
| 1 | 2 | 6 | 5/4 | 1/4 | C#3 | ^C, |
| 1 | 2 | 6 | 3/2 | 1/4 | E3 | E, |
| 1 | 2 | 6 | 7/4 | 1/4 | G#3 | ^G, |
| 1 | 2 | 6 | 2 | 1/4 | C#4 | ^C |
| 1 | 2 | 6 | 9/4 | 1/4 | E3 | E, |
| 1 | 2 | 6 | 5/2 | 1/4 | G#3 | ^G, |
| 1 | 2 | 6 | 3 | 1 | REST | z4 |
| 2 | 1 | 1 | 0 | 1/4 | G#4 | ^G |
| 2 | 1 | 1 | 1/4 | 1/4 | C#4 | ^C |
| 2 | 1 | 1 | 1/2 | 1/4 | E4 | E |
| 2 | 1 | 1 | 3/4 | 1/4 | G#4 | ^G |
| 2 | 1 | 1 | 1 | 1/4 | C#5 | ^c |
| 2 | 1 | 1 | 5/4 | 1/4 | E4 | E |
| 2 | 1 | 1 | 3/2 | 1/4 | G#4 | ^G |
| 2 | 1 | 1 | 7/4 | 1/4 | C#5 | ^c |
| 2 | 1 | 1 | 2 | 1/4 | E5 | e |
| 2 | 1 | 1 | 9/4 | 1/4 | G#4 | ^G |
| 2 | 1 | 1 | 5/2 | 1/4 | C#5 | ^c |
| 2 | 1 | 1 | 11/4 | 1/4 | E5 | e |
| 2 | 1 | 1 | 3 | 1/2 | G#4+C#5+E5+G#5 | [^G^ce^g]2 |

---

## Notes / limitations
- This conversion is based on **MusicXML**, so pitch and rhythm should be accurate.
- I skipped **grace notes** (duration=0) in the ABC export; if you want them included, tell me and I’ll regenerate.
- “Both hands” is interpreted as **treble staff = RH** and **bass staff = LH**.  
  The source contains **multiple voices** (e.g., LH5 vs LH6) and occasional cross-staff notes, so the *simplified* file keeps the main playable structure while the *allvoices* file preserves everything.

