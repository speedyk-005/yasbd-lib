import difflib
from functools import cache
from importlib import import_module
from pathlib import Path

from yasbd.exceptions import LangPackError, UnsupportedLanguageError
from yasbd.rules.base import Rules
from yasbd.utils.input_validator import validate_input

# Language packs loaded via register_lang_packs() register their profiles here.
# Maps language code (e.g. "hi") to the Rules subclass.
_LANG_PACK_REGISTRY: dict[str, type[Rules]] = {}


def _validate_profile(profile: type, name: str) -> None:
    """Validate a Rules subclass and smoke-test it.

    Checks that the profile inherits from ``Rules``, can be instantiated,
    and that ``apply()`` returns a list of integers without crashing.
    """
    if not issubclass(profile, Rules):
        raise TypeError(
            f"Profile {profile.__name__!r} in module {name!r} does not inherit from Rules."
        )

    instance = profile()
    result = instance.apply("Hello world.", preserve_quote_and_paren=True)
    if not isinstance(result, list) or not all(isinstance(i, int) for i in result):
        raise TypeError(
            f"Handshake failed for {profile.__name__!r}: "
            f"apply() returned {type(result).__name__}, expected list[int]"
        )


@validate_input
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
                _validate_profile(profile, name)
                lang_code = profile.__name__.removesuffix("Rules").lower()
                _LANG_PACK_REGISTRY[lang_code] = profile
            except (TypeError, RuntimeError) as e:
                raise LangPackError(
                    f"Validation failed for {profile.__name__!r} in module {name!r}.\n"
                    f"Details: {str(e)}"
                ) from e

    get_supported_langs.cache_clear()


def clear_lang_packs() -> None:
    """Remove all registered language packs and reset the supported-languages cache."""
    _LANG_PACK_REGISTRY.clear()
    get_supported_langs.cache_clear()


@cache
def get_supported_langs() -> list[str]:
    """Discover and cache supported language codes.

    Returns a sorted list of ``auto`` plus all language codes from
    the built-in rules directory and any registered language packs.
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
