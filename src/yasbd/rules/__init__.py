import difflib
import re
from functools import cache
from importlib import import_module
from pathlib import Path

from yasbd.exceptions import PluginError, UnsupportedLanguageError, YasbdError
from yasbd.rules.base import Rules

# Plugins loaded via register_plugins() register their Profiles here.
# Maps language code (e.g. "hi") to the Rules subclass.
_PLUGIN_REGISTRY: dict[str, type[Rules]] = {}


def _handshake_profile(profile: Rules) -> None:
    """Smoke-test the profile by running ``apply()`` on mock text.

    Ensures the profile doesn't crash on basic input before registration.
    """
    try:
        profile.apply("Hello world.", preserve_quote_and_paren=True)
    except Exception as e:
        raise PluginError(f"Handshake failed for {type(profile).__name__!r}: {e}") from e


def register_plugins(names: list[str]) -> None:
    """Import and validate external language plugin modules.

    Each module must expose a ``PROFILES`` list of ``Rules`` subclasses.
    All validated profiles are stored in ``_PLUGIN_REGISTRY``.

    Args:
        names: Module names resolvable from the Python path
            (e.g. ``["yasbd_indic", "yasbd_legal"]``).

    Raises:
        YasbdError: If a plugin module cannot be imported.
    """
    for name in names:
        try:
            mod = import_module(name)
        except ImportError as e:
            raise PluginError(
                f"Plugin module {name!r} could not be imported. "
                "Make sure it is installed and on the Python path.\n"
                f"💡 Try: pip install {name}"
            ) from e

        profiles = getattr(mod, "PROFILES", None)
        if profiles is None:
            raise PluginError(f"Plugin module {name!r} has no PROFILES list.")

        for profile in profiles:
            try:
                instance = profile()
                _handshake_profile(instance)
                lang_code = profile.__name__.removesuffix("Rules").lower()
                _PLUGIN_REGISTRY[lang_code] = profile
            except Exception as e:
                raise PluginError(
                    f"Validation failed for {profile.__name__!r} in plugin {name!r}."
                ) from e


@cache
def get_supported_langs() -> list[str]:
    """Discover and cache supported language codes

    It returns a list containing the rules from the rules directory
    plus the plugins versions.
    """
    rules_dir = Path(__file__).parent
    langs = list(_PLUGIN_REGISTRY.keys())
    for f in rules_dir.iterdir():
        if f.stem in ("_template", "base", "__init__"):
            continue
        if f.suffix == ".py":
            langs.append(f.stem)
    return ["auto"] + sorted(langs)


def load_rule(lang: str) -> Rules:
    """Import and instantiate the rule module for *lang*.

    Checks the plugin registry first; falls back to the built-in rules directory.

    Returns:
        The instantiated rule object.

    Raises:
        UnsupportedLanguageError: If no rule module exists for *lang*.
    """
    if profile_cls := _PLUGIN_REGISTRY.get(lang):
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
