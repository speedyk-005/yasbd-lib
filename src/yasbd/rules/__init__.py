from functools import cache
from pathlib import Path


@cache
def get_supported_langs() -> list[str]:
    """Discover and cache supported language codes from the rules directory."""
    rules_dir = Path(__file__).parent
    langs: list[str] = []
    for f in rules_dir.iterdir():
        if f.stem in ("_template", "base", "__init__"):
            continue
        if f.suffix == ".py":
            langs.append(f.stem)
    return sorted(langs)
