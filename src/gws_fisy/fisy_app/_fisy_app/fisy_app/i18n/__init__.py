from importlib.resources import files
import json

def load_langs():
    langs = {}
    pkg = files(__package__)
    for p in pkg.iterdir():
        if p.name.endswith(".json"):
            langs[p.name[:-5]] = json.loads(p.read_text(encoding="utf-8"))
    return langs

LANGS = load_langs()
