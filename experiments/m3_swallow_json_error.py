import json
import os

class ConfigLoader:
    def load(self, path: str) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config {path} not found")
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
