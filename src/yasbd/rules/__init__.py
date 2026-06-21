import difflib
from functools import cache
from importlib import import_module
from pathlib import Path

from yasbd.exceptions import UnsupportedLanguageError
from yasbd.rules.base import Rules


@cache
def get_supported_langs() -> list[str]:
    """Discover and cache supported language codes from the rules directory."""
    rules_dir = Path(__file__).parent
    langs = []
    for f in rules_dir.iterdir():
        if f.stem in ("_template", "base", "__init__"):
            continue
        if f.suffix == ".py":
            langs.append(f.stem)
    return ["auto"] + sorted(langs)


def load_rule(lang: str) -> Rules:
    """Import and instantiate the rule module for *lang*.

    Returns:
        The instantiated rule object.

    Raises:
        UnsupportedLanguageError: If no rule module exists for *lang*.
    """
    try:
        rule_module = import_module(f"yasbd.rules.{lang}")
    except ModuleNotFoundError as e:
        if lang not in str(e):
            raise
        supported = get_supported_langs()
        msg = (
            f"{lang!r} doesn't fit any cutting profile I know.\n"
            f"Supported language codes:\n  {' · '.join(supported)}"
        )
        if close := difflib.get_close_matches(lang, supported, n=3, cutoff=0.5):
            msg += f"\n\n💭 Perhaps you meant {' or '.join(repr(c) for c in close)}?"
        raise UnsupportedLanguageError(msg) from None

    return getattr(rule_module, f"{lang.capitalize()}Rules")()
