## Add language pack system with handshake validation and registry

### Summary

Introduces a lightweight lang pack system for external language profiles. Instead of forking the repo to add private rules, users can now ship them as standalone Python packages and register them at runtime.

### Changes

**New: `LangPackError` exception class** (`exceptions.py`)
- Raised when a lang pack module fails import, validation, or handshake.

**New: lang pack machinery** (`src/yasbd/rules/__init__.py`)
- `register_lang_packs(names)` — imports modules by name, validates they expose a `PROFILES` list, runs each profile through a handshake smoke test (`apply("Hello world.")`), and stores them in `_LANG_PACK_REGISTRY`.
- `_LANG_PACK_REGISTRY` — dict mapping language code → Rules subclass, checked first by `load_rule()` before falling back to built-in rules.
- `_handshake_profile()` — smoke-test that ensures a profile doesn't crash on basic input before it's registered.

**Assertion guard** — each profile is checked with `assert issubclass(profile, Rules)` before instantiation, producing a clear error message if someone drops a random class into `PROFILES`. The assert lives outside the try/except so the traceback stays visible.

**Lang pack contract** — a module must expose:
```python
PROFILES = [HindiMyRules, BengaliMyRules]  # list of Rules subclasses
```

**Tested** — 5 tests covering:
- Unresolvable module → `LangPackError`
- Module without `PROFILES` → `LangPackError`
- Non-`Rules` class in `PROFILES` → `LangPackError`
- Happy path: register + load
- Lang pack takes precedence over built-in language code

### Docs
- README: new **Lang Packs** section with usage example and link to `_template.py`.
- Roadmap: external language packs marked done.
- CHANGELOG updated.

### Usage

```python
from yasbd import BoundaryDetector
from yasbd.rules import register_lang_packs

register_lang_packs(["my_yasbd_indic"])
detector = BoundaryDetector("hi")  # loads from lang pack if registered
```
