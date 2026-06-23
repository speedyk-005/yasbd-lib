import difflib
import re
from functools import cache
from importlib import import_module
from pathlib import Path

from beartype.door import die_if_unbearable

from yasbd.exceptions import LangPackError, UnsupportedLanguageError, YasbdError
from yasbd.rules.base import Rules

# Language packs loaded via register_lang_packs() register their profiles here.
# Maps language code (e.g. "hi") to the Rules subclass.
_LANG_PACK_REGISTRY: dict[str, type[Rules]] = {}


def _handshake_profile(profile: Rules) -> None:
    """Smoke-test the profile by running ``apply()`` on mock text.

    Ensures the profile doesn't crash on basic input and that
    ``apply()`` returns a list of integers before registration.
    """
    try:
        result = profile.apply("Hello world.", preserve_quote_and_paren=True)
        die_if_unbearable(result, list[int])
    except Exception as e:
        raise LangPackError(f"Handshake failed for {type(profile).__name__!r}: {e}") from e


def register_lang_packs(names: list[str]) -> None:
    """Import and validate external language pack modules.

    Each module must expose a ``PROFILES`` list of ``Rules`` subclasses.
    All validated profiles are stored in ``_LANG_PACK_REGISTRY``.

    Caution:
        This function imports arbitrary Python modules by name. Only load lang
        packs from sources you trust — an untrusted module can execute
        arbitrary code at import time.

    Args:
        names: Module names resolvable from the Python path
            (e.g. ``["yasbd_indic", "yasbd_legal"]``).

    Raises:
        LangPackError: If a language pack module cannot be imported.
    """
    for name in names:
        try:
            mod = import_module(name)
        except ImportError as e:
            raise LangPackError(
                f"Language pack module {name!r} could not be imported. "
                "Make sure it is installed and on the Python path.\n"
                f"💡 Try: pip install {name}"
            ) from e

        profiles = getattr(mod, "PROFILES", None)
        if profiles is None:
            raise LangPackError(
                f"Language pack module {name!r} has no PROFILES list. "
                "Each language pack module must expose a PROFILES list of Rules subclasses."
            )

        for profile in profiles:
            try:
                assert issubclass(profile, Rules), "Must inherit from yasbd.rules.Rules"
                instance = profile()
                _handshake_profile(instance)
                lang_code = profile.__name__.removesuffix("Rules").lower()
                _LANG_PACK_REGISTRY[lang_code] = profile
            except Exception as e:
                raise LangPackError(
                    f"Validation failed for {profile.__name__!r} in module {name!r}.\n"
                    f"Details: {str(e)}"
                ) from e


def clear_lang_packs() -> None:
    """Remove all registered language packs from the registry."""
    _LANG_PACK_REGISTRY.clear()
    get_supported_langs.cache_clear()


@cache
def get_supported_langs() -> list[str]:
    """Discover and cache supported language codes

    It returns a list containing the rules from the rules directory
    plus the language pack versions.
    """
    rules_dir = Path(__file__).parent
    langs = set(_LANG_PACK_REGISTRY.keys())
    for f in rules_dir.iterdir():
        if f.stem in ("_template", "base", "__init__"):
            continue
        if f.suffix == ".py":
            langs.add(f.stem)
    return ["auto"] + sorted(langs)


def load_rule(lang: str) -> Rules:
    """Import and instantiate the rule module for *lang*.

    Checks the language pack registry first; falls back to the built-in rules directory.

    Returns:
        The instantiated rule object.

    Raises:
        UnsupportedLanguageError: If no rule module exists for *lang*.
    """
    if profile_cls := _LANG_PACK_REGISTRY.get(lang):
        return profile_cls()

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
