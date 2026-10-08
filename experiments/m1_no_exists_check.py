import json
import os

class ConfigLoader:
    def load(self, path: str) -> dict:
        with open(path, 'r') as f:
            return json.load(f)
