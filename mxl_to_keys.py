#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict

from music21 import chord, converter, meter, note, pitch, stream

EPSILON = 1e-9


def pitch_to_token(p: pitch.Pitch) -> str:
    """Convert a music21 pitch into a compact token like c4 or f##5."""
    step = p.step.lower() if p.step else p.name[0].lower()
    accidental = ""
    if p.accidental is not None and p.accidental.modifier:
        accidental = p.accidental.modifier.replace("-", "b")
    octave = "" if p.octave is None else str(p.octave)
    return f"{step}{accidental}{octave}"


def element_to_token(element: note.NotRest) -> str:
    if isinstance(element, note.Note):
        return pitch_to_token(element.pitch)
    if isinstance(element, chord.Chord):
        chord_tokens = [pitch_to_token(p) for p in sorted(element.pitches, key=lambda p: p.midi or -1)]
        return f"[{' '.join(chord_tokens)}]"
    raise TypeError(f"Unsupported element type: {type(element)}")


def _is_hidden_rest(rest: note.Rest) -> bool:
    return bool(getattr(rest.style, "hideObjectOnPrint", False))


def extract_part_tokens(file_path: str, include_rests: bool = False) -> Dict[int, list[str]]:
    score = converter.parse(file_path)
    parts = list(score.parts) or [score]
    part_tokens: Dict[int, list[str]] = {}

    for idx, part in enumerate(parts, start=1):
        tokens: list[str] = []
        for element in part.flatten().notesAndRests:
            if isinstance(element, note.Rest):
                if include_rests and not _is_hidden_rest(element):
                    tokens.append("rest")
                continue
            if isinstance(element, (note.Note, chord.Chord)):
                tokens.append(element_to_token(element))
        part_tokens[idx] = tokens

    return part_tokens


def format_part_lines(part_tokens: Dict[int, list[str]]) -> str:
    lines = []
    for idx in sorted(part_tokens):
        joined = " ".join(part_tokens[idx])
        lines.append(f"part {idx}: {joined}".rstrip())
    return "\n".join(lines)


def _measure_to_beat_cells(measure: stream.Measure, steps_per_beat: int = 4) -> list[str]:
    ts = measure.timeSignature or measure.getContextByClass(meter.TimeSignature)
    beat_quarter_length = 1.0
    measure_quarter_length = 4.0

    if ts is not None:
        beat_quarter_length = float(ts.beatDuration.quarterLength or 1.0)
        measure_quarter_length = float(ts.barDuration.quarterLength or measure.duration.quarterLength or 4.0)
    elif measure.duration.quarterLength:
        measure_quarter_length = float(measure.duration.quarterLength)

    beat_count = max(1, int(round(measure_quarter_length / beat_quarter_length)))
    step_quarter_length = beat_quarter_length / steps_per_beat
    total_steps = beat_count * steps_per_beat

    onset_map: dict[int, list[str]] = defaultdict(list)
    active_spans: list[tuple[float, float]] = []

    for element in measure.recurse().notesAndRests:
        start = float(element.offset)
        if start >= measure_quarter_length - EPSILON:
            continue

        duration = float(element.quarterLength)
        if duration <= EPSILON:
            continue

        end = min(start + duration, measure_quarter_length)

        if isinstance(element, (note.Note, chord.Chord)):
            step_index = int(round(start / step_quarter_length))
            if 0 <= step_index < total_steps:
                onset_map[step_index].append(element_to_token(element))
            active_spans.append((start, end))

    step_tokens: list[str] = []
    for step_index in range(total_steps):
        current_time = step_index * step_quarter_length
        onsets = onset_map.get(step_index)
        if onsets:
            if len(onsets) == 1:
                step_tokens.append(onsets[0])
            else:
                step_tokens.append(f"[{' '.join(onsets)}]")
            continue

        is_hold = any(start + EPSILON < current_time < end - EPSILON for start, end in active_spans)
        step_tokens.append("—" if is_hold else "·")

    beat_cells: list[str] = []
    for beat_index in range(beat_count):
        start = beat_index * steps_per_beat
        end = start + steps_per_beat
        beat_cells.append(" ".join(step_tokens[start:end]))

    return beat_cells


def _hand_label(part_index: int) -> str:
    if part_index == 1:
        return "RH"
    if part_index == 2:
        return "LH"
    return f"P{part_index}"


def generate_markdown_table(file_path: str, steps_per_beat: int = 4) -> str:
    if steps_per_beat < 1:
        raise ValueError("steps_per_beat must be >= 1")

    score = converter.parse(file_path)
    parts = list(score.parts) or [score]

    measure_numbers: list[int] = []
    for part in parts:
        for measure in part.getElementsByClass(stream.Measure):
            if measure.number is not None:
                measure_numbers.append(int(measure.number))

    if not measure_numbers:
        return "# Practice Table\n\nNo measures found.\n"

    unique_measures = sorted(set(measure_numbers))
    rows: list[tuple[int, str, list[str]]] = []
    max_beats = 1

    for measure_number in unique_measures:
        for part_index, part in enumerate(parts, start=1):
            measure = part.measure(measure_number)
            if measure is None:
                continue
            cells = _measure_to_beat_cells(measure, steps_per_beat=steps_per_beat)
            max_beats = max(max_beats, len(cells))
            rows.append((measure_number, _hand_label(part_index), cells))

    beat_headers = [f"Beat {idx}" for idx in range(1, max_beats + 1)]
    placeholder_cell = " ".join(["·"] * steps_per_beat)

    lines = [
        f"# {Path(file_path).stem} - Practice Grid",
        "",
        f"Format: each beat has {steps_per_beat} mini-steps. `·` = rest, `—` = hold, `[ ... ]` = chord.",
        "",
        "| M | Hand | " + " | ".join(beat_headers) + " |",
        "|---:|:----:|" + "|".join([":------" for _ in beat_headers]) + "|",
    ]

    for measure_number, hand, cells in rows:
        padded_cells = cells + [placeholder_cell] * (max_beats - len(cells))
        lines.append(f"| {measure_number} | {hand} | " + " | ".join(padded_cells) + " |")

    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert .mxl/.musicxml into readable key tokens such as c4 and [c4 e4 g4]."
    )
    parser.add_argument("input", type=Path, help="Path to .mxl or .musicxml file")
    parser.add_argument("-o", "--output", type=Path, help="Optional output text file path")
    parser.add_argument(
        "--include-rests",
        action="store_true",
        help="Include rest events as the token 'rest'",
    )
    parser.add_argument(
        "--markdown-table",
        action="store_true",
        help="Output a measure-by-measure Markdown practice table (RH/LH rows, beat cells).",
    )
    parser.add_argument(
        "--steps-per-beat",
        type=int,
        default=4,
        help="Mini-step resolution for --markdown-table (default: 4).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.markdown_table:
        output = generate_markdown_table(str(args.input), steps_per_beat=args.steps_per_beat)
    else:
        part_tokens = extract_part_tokens(str(args.input), include_rests=args.include_rests)
        output = format_part_lines(part_tokens)

    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
