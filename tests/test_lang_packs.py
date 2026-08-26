import sys
import types

import pytest

from yasbd import BoundaryDetector
from yasbd.exceptions import LangPackError
from yasbd.rules import load_external_lang_packs, load_rule
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
    """Clean up injected modules after each test."""
    yield
    for name in list(sys.modules):
        if name.startswith("_test_lang_pack_"):
            del sys.modules[name]


def test_import_error():
    """Test that load_external_lang_packs raises error for an unresolvable module."""
    with pytest.raises(LangPackError, match="could not be imported"):
        load_external_lang_packs(["_test_lang_pack_nonexistent"], {})


def test_no_profiles():
    """Test that load_external_lang_packs raises error when a module has no PROFILES."""
    _make_fake_lang_pack("_test_lang_pack_noprofiles")
    with pytest.raises(LangPackError, match="has no PROFILES list"):
        load_external_lang_packs(["_test_lang_pack_noprofiles"], {})


def test_non_rules_profile():
    """Test that load_external_lang_packs rejects a non-Rules subclass in PROFILES."""

    class NotRules:
        def apply(self, text, _preserve_quote_and_paren):
            return [len(text)]

    _make_fake_lang_pack("_test_lang_pack_notrules", profiles=[NotRules])
    with pytest.raises(LangPackError, match="Validation failed for 'NotRules'"):
        load_external_lang_packs(["_test_lang_pack_notrules"], {})


def test_handshake_override_apply():
    """Test that load_external_lang_packs rejects a profile overriding apply()."""

    class WrongReturn(Rules):
        def apply(self, _text, _preserve_quote_and_paren):
            return "not a list"

    _make_fake_lang_pack("_test_lang_pack_wrong_return", profiles=[WrongReturn])
    with pytest.raises(LangPackError, match="must not override apply"):
        load_external_lang_packs(["_test_lang_pack_wrong_return"], {})


def test_register_and_load():
    """Test that load_external_lang_packs stores a profile and load_rule returns an instance."""

    class FakeRules(Rules):
        pass

    registry: dict = {}
    _make_fake_lang_pack("_test_lang_pack_load", profiles=[FakeRules])
    load_external_lang_packs(["_test_lang_pack_load"], registry)
    assert "fake" in registry, "Profile not registered"
    assert registry["fake"][1] is FakeRules, "Wrong class in registry"
    instance = load_rule("fake", ext_registry=registry)
    assert isinstance(instance, FakeRules), "load_rule returned wrong type"


def test_lang_pack_takes_precedence():
    """Test that a lang pack profile overrides a built-in language code."""

    class EnRules(Rules):
        pass

    registry: dict = {}
    _make_fake_lang_pack("_test_lang_pack_override", profiles=[EnRules])
    load_external_lang_packs(["_test_lang_pack_override"], registry)
    instance = load_rule("en", ext_registry=registry)
    assert isinstance(instance, EnRules), "Lang pack did not override built-in EnRules"


def test_no_registry_still_validates():
    """Test that load_external_lang_packs validates without a registry."""

    class FakeRules(Rules):
        pass

    _make_fake_lang_pack("_test_lang_pack_noreg", profiles=[FakeRules])
    registered = load_external_lang_packs(["_test_lang_pack_noreg"])
    assert registered == ["fake"]


def test_boundary_detector_with_external_lang_packs():
    """Test that BoundaryDetector loads external packs via external_lang_packs param."""

    class FakeRules(Rules):
        pass

    _make_fake_lang_pack("_test_lang_pack_bd", profiles=[FakeRules])
    detector = BoundaryDetector(lang="fake", external_lang_packs=["_test_lang_pack_bd"])
    assert detector.lang == "fake"
    rule = detector._get_rule("fake")
    assert isinstance(rule, FakeRules), "BoundaryDetector did not load external pack"
