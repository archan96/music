import subprocess
import tempfile
import unittest
from pathlib import Path

from music21 import chord, meter, note, stream

import mxl_to_keys


class MxlToKeysTests(unittest.TestCase):
    def test_note_token_is_lowercase_with_octave(self):
        n = note.Note("C#4")
        self.assertEqual(mxl_to_keys.element_to_token(n), "c#4")

    def test_chord_token_is_bracketed(self):
        c = chord.Chord(["G4", "C4", "E4"])
        self.assertEqual(mxl_to_keys.element_to_token(c), "[c4 e4 g4]")

    def test_extract_part_tokens_from_musicxml(self):
        with tempfile.TemporaryDirectory() as tmp:
            xml_path = Path(tmp) / "sample.musicxml"

            score = stream.Score()
            rh = stream.Part(id="RH")
            lh = stream.Part(id="LH")

            rh.append(note.Note("C4", quarterLength=1))
            rh.append(chord.Chord(["E4", "G4"], quarterLength=1))
            rh.append(note.Rest(quarterLength=1))

            lh.append(note.Note("C3", quarterLength=1))
            lh.append(note.Rest(quarterLength=1))

            score.insert(0, rh)
            score.insert(0, lh)
            score.write("musicxml", fp=str(xml_path))

            parts_no_rest = mxl_to_keys.extract_part_tokens(str(xml_path))
            self.assertEqual(parts_no_rest, {1: ["c4", "[e4 g4]"], 2: ["c3"]})

            parts_with_rest = mxl_to_keys.extract_part_tokens(str(xml_path), include_rests=True)
            self.assertEqual(parts_with_rest, {1: ["c4", "[e4 g4]", "rest"], 2: ["c3", "rest"]})

    def test_cli_prints_part_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            xml_path = Path(tmp) / "sample.musicxml"
            out_dir = Path(tmp) / "out-keys"

            score = stream.Score()
            p = stream.Part(id="P1")
            p.append(note.Note("D4", quarterLength=1))
            p.append(note.Note("E4", quarterLength=1))
            score.insert(0, p)
            score.write("musicxml", fp=str(xml_path))

            proc = subprocess.run(
                [
                    str(Path.cwd() / ".venv" / "bin" / "python"),
                    str(Path.cwd() / "mxl_to_keys.py"),
                    str(xml_path),
                    "--output-dir",
                    str(out_dir),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            output_path = out_dir / "sample.keys.txt"
            self.assertTrue(output_path.exists())
            self.assertIn("part 1: d4 e4", output_path.read_text(encoding="utf-8"))

    def test_generate_markdown_table_has_rh_lh_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            xml_path = Path(tmp) / "sample.musicxml"

            score = stream.Score()

            rh = stream.Part(id="RH")
            m1_rh = stream.Measure(number=1)
            m1_rh.append(meter.TimeSignature("4/4"))
            m1_rh.append(note.Note("C4", quarterLength=1))
            m1_rh.append(note.Rest(quarterLength=1))
            m1_rh.append(chord.Chord(["E4", "G4"], quarterLength=2))
            rh.append(m1_rh)

            lh = stream.Part(id="LH")
            m1_lh = stream.Measure(number=1)
            m1_lh.append(meter.TimeSignature("4/4"))
            m1_lh.append(note.Note("C3", quarterLength=4))
            lh.append(m1_lh)

            score.insert(0, rh)
            score.insert(0, lh)
            score.write("musicxml", fp=str(xml_path))

            markdown = mxl_to_keys.generate_markdown_table(str(xml_path))
            self.assertIn("| M | Hand | Beat 1 | Beat 2 | Beat 3 | Beat 4 |", markdown)
            self.assertIn("| 1 | RH | c4 — — — | · · · · | [e4 g4] — — — | — — — — |", markdown)
            self.assertIn("| 1 | LH | c3 — — — | — — — — | — — — — | — — — — |", markdown)

    def test_cli_markdown_table_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            xml_path = Path(tmp) / "sample.musicxml"
            out_dir = Path(tmp) / "out-grid"

            score = stream.Score()
            p1 = stream.Part(id="P1")
            m1 = stream.Measure(number=1)
            m1.append(meter.TimeSignature("4/4"))
            m1.append(note.Note("D4", quarterLength=4))
            p1.append(m1)
            score.insert(0, p1)
            score.write("musicxml", fp=str(xml_path))

            proc = subprocess.run(
                [
                    str(Path.cwd() / ".venv" / "bin" / "python"),
                    str(Path.cwd() / "mxl_to_keys.py"),
                    str(xml_path),
                    "--markdown-table",
                    "--output-dir",
                    str(out_dir),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            output_path = out_dir / "sample.practice_grid.md"
            self.assertTrue(output_path.exists())
            self.assertIn("| M | Hand | Beat 1 | Beat 2 | Beat 3 | Beat 4 |", output_path.read_text(encoding="utf-8"))

    def test_extract_part_tokens_from_midi(self):
        with tempfile.TemporaryDirectory() as tmp:
            midi_path = Path(tmp) / "sample.mid"

            score = stream.Score()
            p = stream.Part(id="P1")
            p.append(note.Note("C4", quarterLength=1))
            p.append(note.Note("E4", quarterLength=1))
            p.append(chord.Chord(["G4", "B4"], quarterLength=1))
            score.insert(0, p)
            score.write("midi", fp=str(midi_path))

            parts = mxl_to_keys.extract_part_tokens(str(midi_path))
            self.assertEqual(parts, {1: ["c4", "e4", "[g4 b4]"]})

    def test_generate_markdown_table_from_midi(self):
        with tempfile.TemporaryDirectory() as tmp:
            midi_path = Path(tmp) / "sample.mid"

            score = stream.Score()
            p = stream.Part(id="P1")
            p.append(note.Note("C4", quarterLength=1))
            p.append(note.Note("D4", quarterLength=1))
            p.append(note.Note("E4", quarterLength=1))
            p.append(note.Note("F4", quarterLength=1))
            score.insert(0, p)
            score.write("midi", fp=str(midi_path))

            markdown = mxl_to_keys.generate_markdown_table(str(midi_path))
            self.assertIn("| M | Hand | Beat 1 | Beat 2 | Beat 3 | Beat 4 |", markdown)
            self.assertIn("| 1 | RH | c4 — — — | d4 — — — | e4 — — — | f4 — — — |", markdown)

    def test_midi_wrapper_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            midi_path = Path(tmp) / "sample.mid"
            out_dir = Path(tmp) / "out-keys"

            score = stream.Score()
            p = stream.Part(id="P1")
            p.append(note.Note("C4", quarterLength=1))
            p.append(note.Note("E4", quarterLength=1))
            score.insert(0, p)
            score.write("midi", fp=str(midi_path))

            proc = subprocess.run(
                [
                    str(Path.cwd() / ".venv" / "bin" / "python"),
                    str(Path.cwd() / "midi_to_keys.py"),
                    str(midi_path),
                    "--output-dir",
                    str(out_dir),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            output_path = out_dir / "sample.keys.txt"
            self.assertTrue(output_path.exists())
            self.assertIn("part 1: c4 e4", output_path.read_text(encoding="utf-8"))

    def test_cli_stdout_flag_prints_instead_of_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            midi_path = Path(tmp) / "sample.mid"

            score = stream.Score()
            p = stream.Part(id="P1")
            p.append(note.Note("C4", quarterLength=1))
            p.append(note.Note("D4", quarterLength=1))
            score.insert(0, p)
            score.write("midi", fp=str(midi_path))

            proc = subprocess.run(
                [
                    str(Path.cwd() / ".venv" / "bin" / "python"),
                    str(Path.cwd() / "mxl_to_keys.py"),
                    str(midi_path),
                    "--stdout",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            self.assertIn("part 1: c4 d4", proc.stdout)

    def test_resolve_output_path_defaults(self):
        keys_path = mxl_to_keys.resolve_output_path(
            input_path=Path("data/midi/moonlight1.mid"),
            output_path=None,
            output_dir=None,
            markdown_table=False,
        )
        grid_path = mxl_to_keys.resolve_output_path(
            input_path=Path("data/midi/moonlight1.mid"),
            output_path=None,
            output_dir=None,
            markdown_table=True,
        )
        self.assertEqual(keys_path.as_posix(), "output/keys/moonlight1.keys.txt")
        self.assertEqual(grid_path.as_posix(), "output/practice-grids/moonlight1.practice_grid.md")

    def test_shell_wrapper_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            midi_path = Path(tmp) / "sample.mid"
            out_dir = Path(tmp) / "shell-out"

            score = stream.Score()
            p = stream.Part(id="P1")
            p.append(note.Note("C4", quarterLength=1))
            p.append(note.Note("E4", quarterLength=1))
            score.insert(0, p)
            score.write("midi", fp=str(midi_path))

            proc = subprocess.run(
                [
                    str(Path.cwd() / "convert_music.sh"),
                    str(midi_path),
                    "--out-dir",
                    str(out_dir),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            output_path = out_dir / "sample.keys.txt"
            self.assertTrue(output_path.exists())
            self.assertIn("part 1: c4 e4", output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
