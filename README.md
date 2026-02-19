# music

## Folder structure

```text
music-archan/
├── data/
│   ├── midi/                  # input .mid files
│   └── mxl/                   # input .mxl/.musicxml files
├── output/
│   ├── keys/                  # generated .keys.txt output
│   └── practice-grids/        # generated markdown grids
├── tests/
├── midi_to_keys.py            # midi CLI wrapper
├── mxl_to_keys.py             # core converter CLI
└── README.md
```

## Example usage

```bash
./convert_music.sh ./data/midi/ludovico-einaudi-nuvole-bianche-6901.mid
./convert_music.sh ./data/midi/ludovico-einaudi-nuvole-bianche-6901.mid --grid
./convert_music.sh ./data/mxl/moonlight_sonata_3rd_movement.mxl --grid
```

The converter now auto-generates output filenames from the input filename:

- `output/keys/<input_name>.keys.txt`
- `output/practice-grids/<input_name>.practice_grid.md`

Example:

```bash
./.venv/bin/python mxl_to_keys.py ./data/mxl/moonlight_sonata_3rd_movement.mxl
# Wrote: output/keys/moonlight_sonata_3rd_movement.keys.txt

./.venv/bin/python mxl_to_keys.py ./data/mxl/moonlight_sonata_3rd_movement.mxl --markdown-table
# Wrote: output/practice-grids/moonlight_sonata_3rd_movement.practice_grid.md
```

Optional flags:

```bash
# custom output directory (name still auto-derived)
./convert_music.sh ./data/midi/moonlight1.mid --out-dir ./output/custom

# print to terminal instead of writing a file
./.venv/bin/python mxl_to_keys.py ./data/midi/moonlight1.mid --stdout
```
