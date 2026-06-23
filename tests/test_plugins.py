import sys
import types

import pytest

from yasbd.exceptions import PluginError
from yasbd.rules import _PLUGIN_REGISTRY, load_rule, register_plugins
from yasbd.rules.base import Rules


def _make_fake_plugin(name: str, profiles: list | None = None) -> types.ModuleType:
    """Create a fake plugin module and inject it into sys.modules."""
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
        if name.startswith("_test_plugin_"):
            del sys.modules[name]
    _PLUGIN_REGISTRY.clear()


def test_import_error():
    """Test that register_plugins raises error for an unresolvable module."""
    with pytest.raises(PluginError, match="could not be imported"):
        register_plugins(["_test_plugin_nonexistent"])


def test_no_profiles():
    """Test that register_plugins raises error when a module has no PROFILES."""
    _make_fake_plugin("_test_plugin_noprofiles")
    with pytest.raises(PluginError, match="has no PROFILES list"):
        register_plugins(["_test_plugin_noprofiles"])


def test_non_rules_profile():
    """Test that register_plugins rejects a non-Rules subclass in PROFILES."""

    class NotRules:
        def apply(self, text, preserve_quote_and_paren):
            return [len(text)]

    _make_fake_plugin("_test_plugin_notrules", profiles=[NotRules])
    with pytest.raises(PluginError, match="Validation failed for 'NotRules'"):
        register_plugins(["_test_plugin_notrules"])


def test_register_and_load():
    """Test that register_plugins stores a profile and load_rule returns an instance."""

    class FakeRules(Rules):
        pass

    _make_fake_plugin("_test_plugin_load", profiles=[FakeRules])
    register_plugins(["_test_plugin_load"])
    assert "fake" in _PLUGIN_REGISTRY, "Profile not registered"
    assert _PLUGIN_REGISTRY["fake"] is FakeRules, "Wrong class in registry"
    instance = load_rule("fake")
    assert isinstance(instance, FakeRules), "load_rule returned wrong type"


def test_plugin_takes_precedence():
    """Test that a plugin profile overrides a built-in language code."""

    class EnRules(Rules):
        pass

    _make_fake_plugin("_test_plugin_override", profiles=[EnRules])
    register_plugins(["_test_plugin_override"])
    instance = load_rule("en")
    assert isinstance(instance, EnRules), "Plugin did not override built-in EnRules"
