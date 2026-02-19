#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
SCRIPT="$ROOT_DIR/mxl_to_keys.py"

usage() {
  cat <<'EOF'
Usage:
  ./convert_music.sh <input.{mid,midi,mxl,musicxml}> [--grid] [--stdout] [--out-dir DIR]

Examples:
  ./convert_music.sh ./data/midi/moonlight1.mid
  ./convert_music.sh ./data/mxl/moonlight_sonata_3rd_movement.mxl --grid
  ./convert_music.sh ./data/midi/moonlight1.mid --out-dir ./output/custom
EOF
}

if [[ ${1:-} == "" || ${1:-} == "-h" || ${1:-} == "--help" ]]; then
  usage
  exit 0
fi

INPUT="$1"
shift

ARGS=("$INPUT")

while [[ $# -gt 0 ]]; do
  case "$1" in
    --grid)
      ARGS+=("--markdown-table")
      shift
      ;;
    --stdout)
      ARGS+=("--stdout")
      shift
      ;;
    --out-dir)
      if [[ $# -lt 2 ]]; then
        echo "Error: --out-dir requires a value" >&2
        exit 1
      fi
      ARGS+=("--output-dir" "$2")
      shift 2
      ;;
    *)
      echo "Error: Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

exec "$PYTHON_BIN" "$SCRIPT" "${ARGS[@]}"
