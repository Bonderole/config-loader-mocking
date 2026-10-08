# Контекст: ConfigLoader.load(path) читает JSON-файл.

import json
import os

class ConfigLoader:
    def load(self, path: str) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config {path} not found")
        with open(path, 'r') as f:
            return json.load(f)