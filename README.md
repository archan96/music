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
./.venv/bin/python midi_to_keys.py ./data/midi/ludovico-einaudi-nuvole-bianche-6901.mid --markdown-table -o ./output/practice-grids/ludovico-einaudi-nuvole-bianche.md

./.venv/bin/python mxl_to_keys.py ./data/mxl/moonlight_sonata_3rd_movement.mxl -o ./output/keys/moonlight_sonata_3rd_movement.keys.txt
```
