import json
from pathlib import Path

class ConfigLoader:
    """Рефакторинг без изменения поведения: pathlib вместо os.path и open()."""
    def load(self, path: str) -> dict:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Config {path} not found")
        return json.loads(p.read_text())
