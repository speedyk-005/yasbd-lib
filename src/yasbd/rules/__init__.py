import difflib
from functools import cache
from importlib import import_module
from pathlib import Path

from yasbd.exceptions import LangPackError, UnsupportedLanguageError
from yasbd.utils.logger import log_info
from yasbd.rules.base import Rules


def _validate_profile(profile: type, name: str) -> None:
    """Validate a Rules subclass.

    Checks that the profile inherits from ``Rules`` and does not override
    ``apply()``.
    """
    if not issubclass(profile, Rules):
        raise TypeError(
            f"Profile {profile.__name__!r} in module {name!r} does not inherit from Rules."
        )

    if profile.apply is not Rules.apply:
        raise TypeError(f"Profile {profile.__name__!r} must not override apply().")


def load_external_lang_packs(names: list[str]) -> dict:
    """Import and validate external language pack modules.

    Each module must expose a ``PROFILES`` list of ``Rules`` subclasses.

    Caution:
        This function imports arbitrary Python modules by name. Only load lang
        packs from sources you trust — an untrusted module can execute
        arbitrary code at import time.

    Args:
        names: Module names resolvable from the Python path
            (e.g. ``["yasbd_indic", "yasbd_legal"]``).

    Returns:
        Dict of ``{lang_code: (pack_name, Rules_class)}`` entries.

    Raises:
        LangPackError: If a language pack module cannot be imported.
    """
    registry: dict = {}
    for name in names:
        try:
            mod = import_module(name)
        except ImportError:
            raise LangPackError(
                f"Language pack module {name!r} could not be imported. "
                "Make sure it is installed and on the Python path.\n"
                f"💡 Try: pip install {name}"
            ) from None

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
                registry[lang_code] = (name, profile)
            except (TypeError, RuntimeError) as e:
                raise LangPackError(
                    f"Validation failed for {profile.__name__!r} in module {name!r}.\n"
                    f"Details: {e!s}"
                ) from e

    get_supported_langs.cache_clear()
    return registry


@cache
def get_supported_langs() -> list[str]:
    """Discover and cache supported language codes.

    Returns a sorted list of ``auto`` plus all language codes from
    the built-in rules directory and any registered language packs.
    """
    rules_dir = Path(__file__).parent
    langs = {
        f.stem
        for f in rules_dir.iterdir()
        if f.suffix == ".py" and f.stem not in ("_template", "base", "__init__")
    }
    return ["auto", *sorted(langs)]


def load_rule(lang: str, *, ext_registry: dict, verbose: bool = False) -> Rules:
    """Import and instantiate the rule module for *lang*.

    Checks *ext_registry* first; falls back to the built-in rules directory.

    Args:
        lang: Language code (e.g. ``"en"``, ``"fr"``).
        ext_registry: Dict of ``{lang_code: (pack_name, Rules_class)}``
            entries to check before built-in rules.
        verbose: Enable verbose logging.

    Returns:
        The instantiated rule object.

    Raises:
        UnsupportedLanguageError: If no rule module exists for *lang*.
    """
    if profile_data := ext_registry.get(lang):
        name, cls = profile_data
        log_info(verbose, "{} ({}) is loaded successfully", lang, name)
        return cls()

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

    log_info(verbose, "{} (built-in) is loaded successfully", lang)
    return getattr(rule_module, f"{lang.capitalize()}Rules")()
