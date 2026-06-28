import sys
import types

import pytest

from yasbd.exceptions import LangPackError
from yasbd.rules import _LANG_PACK_REGISTRY, clear_lang_packs, load_rule, register_lang_packs
from yasbd.rules.base import Rules


def _make_fake_lang_pack(name: str, profiles: list | None = None) -> types.ModuleType:
    """Create a fake language pack module and inject it into sys.modules."""
    mod = types.ModuleType(name)
    if profiles is not None:
        mod.PROFILES = profiles
    sys.modules[name] = mod
    return mod


@pytest.fixture(autouse=True)
def _cleanup():
    """Clean up injected modules and registry after each test."""
    yield
    for name in list(sys.modules):
        if name.startswith("_test_lang_pack_"):
            del sys.modules[name]
    clear_lang_packs()


def test_import_error():
    """Test that register_lang_packs raises error for an unresolvable module."""
    with pytest.raises(LangPackError, match="could not be imported"):
        register_lang_packs(["_test_lang_pack_nonexistent"])


def test_no_profiles():
    """Test that register_lang_packs raises error when a module has no PROFILES."""
    _make_fake_lang_pack("_test_lang_pack_noprofiles")
    with pytest.raises(LangPackError, match="has no PROFILES list"):
        register_lang_packs(["_test_lang_pack_noprofiles"])


def test_non_rules_profile():
    """Test that register_lang_packs rejects a non-Rules subclass in PROFILES."""

    class NotRules:
        def apply(self, text, preserve_quote_and_paren):
            return [len(text)]

    _make_fake_lang_pack("_test_lang_pack_notrules", profiles=[NotRules])
    with pytest.raises(LangPackError, match="Validation failed for 'NotRules'"):
        register_lang_packs(["_test_lang_pack_notrules"])


def test_handshake_override_apply():
    """Test that register_lang_packs rejects a profile overriding apply()."""

    class WrongReturn(Rules):
        def apply(self, text, preserve_quote_and_paren):
            return "not a list"

    _make_fake_lang_pack("_test_lang_pack_wrong_return", profiles=[WrongReturn])
    with pytest.raises(LangPackError, match="must not override apply"):
        register_lang_packs(["_test_lang_pack_wrong_return"])


def test_register_and_load():
    """Test that register_lang_packs stores a profile and load_rule returns an instance."""

    class FakeRules(Rules):
        pass

    _make_fake_lang_pack("_test_lang_pack_load", profiles=[FakeRules])
    register_lang_packs(["_test_lang_pack_load"])
    assert "fake" in _LANG_PACK_REGISTRY, "Profile not registered"
    assert _LANG_PACK_REGISTRY["fake"][1] is FakeRules, "Wrong class in registry"
    instance = load_rule("fake")
    assert isinstance(instance, FakeRules), "load_rule returned wrong type"


def test_lang_pack_takes_precedence():
    """Test that a lang pack profile overrides a built-in language code."""

    class EnRules(Rules):
        pass

    _make_fake_lang_pack("_test_lang_pack_override", profiles=[EnRules])
    register_lang_packs(["_test_lang_pack_override"])
    instance = load_rule("en")
    assert isinstance(instance, EnRules), "Lang pack did not override built-in EnRules"


def test_clear_lang_packs():
    """Test that clear_lang_packs empties the registry."""

    class FakeRules(Rules):
        pass

    _make_fake_lang_pack("_test_lang_pack_clear", profiles=[FakeRules])
    register_lang_packs(["_test_lang_pack_clear"])
    assert "fake" in _LANG_PACK_REGISTRY
    clear_lang_packs()
    assert "fake" not in _LANG_PACK_REGISTRY, "Registry was not cleared"
