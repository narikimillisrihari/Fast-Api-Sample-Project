import json
from pathlib import Path

def load_sources(file_path: str = "sources.json") -> list:
    path = Path(file_path)
    if not path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
