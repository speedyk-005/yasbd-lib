# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.4] - 2026-06-03

### Added
- **`_post_process_boundaries` hook**: Language-aware sentence boundary correction without modifying regex core pipeline.
- **StreamCleaner step pipeline control (`steps_to_skip`)**: Selectively disable cleanup stages like OCR normalization, HTML sanitization, whitespace normalization, and mojibake correction.

### Changed
- **Regex architecture refactor in `base.py`**: Promoted local regex patterns into class-level attributes for consistency and reuse.
- **`STREET_ABBRVS` merged into `MID_SENTENCE_ABBRVS`**: Street abbreviations are now strictly non-splitting; English restores boundary logic via post-processing hook.
- **`COMMON_ORG_NOUNS` renamed to `ORG_PROPER_NOUNS`**: Renamed and restricted to proper nouns only.
- **Geopolitical abbreviations normalization**: Standardized casing across languages for consistent detection behavior.

### Fixed
- **Sentence splitting bug after `a.m./p.m.` + date tokens** ([#40](https://github.com/speedyk-005/yasbd-lib/pull/40)): Prevented incorrect segmentation when time tokens precede month/day expressions.
- **Japanese over-matching boundary logic**: Removed invalid `\b` dependency in CJK context.
- **Spanish `Ud.` / `Vd.` context splitting issue** ([#31](https://github.com/speedyk-005/yasbd-lib/pull/31)): Prevents incorrect sentence break when followed by proper nouns.
- **Reference abbreviation bracket edge case** ([#35](https://github.com/speedyk-005/yasbd-lib/pull/35)): Added `[` to lookahead set to prevent false boundary triggers.
- **Time-date pipeline cleanup (English-specific logic)** ([#40](https://github.com/speedyk-005/yasbd-lib/pull/40)): Ensures time/date handling is isolated to English rules without affecting other languages.

## [0.1.3] - 2026-06-01

### Fixed
- **HORIZONTAL_LIST_FINDER over-match**: Single-letter abbreviations (`p.`, `h.`, `s.`) no longer treated as alphabetic list markers. Restricted marker range to `[a-eA-E]`.

## [0.1.2] - 2026-06-01

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
- **Single-quote dialog** ([#23](https://github.com/speedyk-005/yasbd-lib/issues/34 )): No longer splits before the dialogue tag (e.g., `'Is this great?' she said.`).
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
