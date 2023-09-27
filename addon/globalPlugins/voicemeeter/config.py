import json
from pathlib import Path


def config_from_json():
    pn = Path.home() / "Documents" / "Voicemeeter" / "nvda_settings.json"
    data = None
    if pn.exists():
        with open(pn, "r") as f:
            data = json.load(f)
    return data or {}


__config = config_from_json()


def get(name, default=None):
    if name in __config:
        return __config[name]
    return default
