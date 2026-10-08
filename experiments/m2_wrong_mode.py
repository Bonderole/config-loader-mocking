import json
import os

class ConfigLoader:
    def load(self, path: str) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config {path} not found")
        with open(path, 'rb') as f:
            return json.load(f)
