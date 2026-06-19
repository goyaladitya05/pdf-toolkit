from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parents[2] / "static"

MAX_UPLOAD_BYTES = 50 * 1024 * 1024
