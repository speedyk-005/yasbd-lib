# Changelog

---

## [Unreleased]

### Added
- **EN_GOLDEN_DATA.py**: 84-case golden benchmark suite for English accuracy testing.
- **run_golden.py**: Accuracy benchmark runner comparing all 7 libraries against the golden suite.
- **Expanded abbreviation coverage**: Dozens of new abbreviations across all categories (TITLE, REFERENCE, DATE, MID_SENTENCE, STREET, NAMES_WITH_EXCLAMATION).

### Changed
- **Trie-based pattern building**: Replaced sorted `"|".join()` with `retrie.Trie` for optimized abbreviation regex generation.
- **Benchmarks rewrite**: Cold/warm tables and all 8 scenario tables updated with real measured timings; accuracy table and conclusion added.
- **Abbreviation redistribution**: Moved shared abbreviations (`fr`, `ing`, `messrs`, `mlle`, `mme`, etc.) from language-specific rules to base class; added language-specific additions in en.py, fr.py, es.py.
- **Pydantic lower bound relaxed**: `>=2.11.0` (was `>=2.12.2`).

### Fixed
- **`ModuleNotFoundError` masking**: `boundary_detector.py` no longer masks unrelated import errors when the language *is* found but a sub-dependency is missing.
- **P.M. false positive**: All-caps `P.M.` no longer caught by acronym pattern; hardcoded exclusion of `p\.m` and `a\.m` in the acronym regex.

---

## [0.1.1] - 2026-05-30

### Fixed
- **Single-quote dialog**: No longer splits before the dialogue tag (e.g., `'Is this great?' she said.`). ([#23])
- **Ellipsis mid-thought**: Three-dot ellipsis (`...`) no longer splits mid-sentence. Only four dots are sentence boundaries.
- **Initialism detection**: Pronoun `I` no longer triggers false splits in names like `Albert I. Jones`.
- **N° reference**: Added to reference abbreviations to prevent split in `N°. 1026.253.553.`

### Changed
- **HORIZONTAL_LIST_FINDER**: Switched to `re2` for lookbehind support. Uses `\b` + negative lookbehind for capitalized words instead of requiring a terminator prefix. Supports other scripts via `\p{Ll}`.

---

## [0.1.0] - 2026-05-29

Initial release.

- **5 languages**: English, French, Spanish, Haitian Creole, Japanese
- **2-pass algorithm**: Pre-processing (double abbreviations, names, lists) + main split via lookbehind-based abbreviation guard
- **Performance**: ~16.5× faster than pysbd on 10.8K character benchmarks
- **pysbd adapter**: Drop-in `Segmenter` compatible with pysbd's API (`segment()`, `clean`, `char_span`)
- **Dual API**: `detect()` for raw boundary offsets, `segment()` for sentence strings with `TextSpan` support
- **Benchmarks**: 7-library comparison across 5 languages and 7 edge cases
