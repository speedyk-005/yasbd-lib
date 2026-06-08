# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.0] - 2026-06-08

### Added
- **Five new languages** ([#48](https://github.com/speedyk-005/yasbd-lib/pull/48), [#54](https://github.com/speedyk-005/yasbd-lib/pull/54)): Russian (ru), Arabic (ar), Chinese (zh), German (de), and Portuguese (pt)
- **Base abbreviation expansion**: Added `diag` to `REFERENCE_ABBRVS`.
- **`Rules.apply` early return**: Added guard for empty/whitespace-only input to skip processing.

### Changed
- **`NAIVE_BOUNDARY_FINDER` cluster logic unification**: Merged contiguous terminator handling into the lookahead assertion for more consistent behavior and fewer edge-case bugs.
- **`FULLWIDTH_GEOPOLITICAL_ABBRVS` moved to class-level attribute** with dynamic regex matching instead of static sets.
- **`COMMON_SENT_STARTERS` expanded** with time-related adverbs (Then, Afterwards, Later, etc.) across all 9 languages.
- **`BoundaryDetector.detect` refactored**: Simplified paragraph iteration logic to reduce cognitive complexity from 20.

### Fixed
- **Full-width geopolitical abbreviation over-matching**: Replaced static set with dynamic regex to prevent false splits in mixed-script text.
- **Acronym/initialism boundary constraint**: Simplified lookbehind to `[.\s]` to reduce false positive matches in edge cases.
- **Superscript indicator false splits**: Added protection to prevent boundary breaks after ordinal markers.
- **Em-dash quoted text splitting**: Added em-dash pattern to `QUOTE_AND_PAREN_FINDER` so dialogue quoted with dashes (`—text! —`) is no longer split prematurely.
- **Newline boundary handling** ([#64](https://github.com/speedyk-005/yasbd-lib/pull/64)): Added `\n` to `NAIVE_BOUNDARY_FINDER` and updated `NEWLINE_INSIDE_SENTENCE_FINDER` to recognize `>` continuation, preventing markdown heading merging.

## [0.2.0] - 2026-06-04

### Added
- **`_post_process_boundaries` hook** ([#39](https://github.com/speedyk-005/yasbd-lib/pull/39)): Language-aware sentence boundary correction without modifying regex core pipeline.
- **StreamCleaner step pipeline control (`steps_to_skip`)** ([#41](https://github.com/speedyk-005/yasbd-lib/pull/41)): Selectively disable cleanup stages like OCR normalization, HTML sanitization, whitespace normalization, and mojibake correction.

### Changed
- **Regex architecture refactor in `base.py`**: Promoted local regex patterns into class-level attributes for consistency and reuse.
- **`STREET_ABBRVS` merged into `MID_SENTENCE_ABBRVS`**: Street abbreviations are now strictly non-splitting; English restores boundary logic via post-processing hook.
- **`COMMON_ORG_NOUNS` renamed to `ORG_PROPER_NOUNS`**: Renamed and restricted to proper nouns only.
- **Geopolitical abbreviations normalization**: Standardized casing across languages for consistent detection behavior.

### Fixed
- **Multilingual structural heading detection** ([#44](https://github.com/speedyk-005/yasbd-lib/pull/44)): Prevents structural headings from triggering false sentence splits in EN, ES, FR, and HT context. Fixes [#36](https://github.com/speedyk-005/yasbd-lib/issues/36).
- **Sentence splitting after mixed-case scientific units** ([#42](https://github.com/speedyk-005/yasbd-lib/pull/42)): Fixes boundary suppression caused by treating mixed-case units (e.g., `meV.`, `kV.`) as standard abbreviations. Fixes [#33](https://github.com/speedyk-005/yasbd-lib/issues/33).
- **Sentence splitting bug after `a.m./p.m.` + date tokens** ([#40](https://github.com/speedyk-005/yasbd-lib/pull/40)): Prevented incorrect segmentation when time tokens precede month/day expressions.
- **Japanese over-matching boundary logic**: Removed invalid `\b` dependency in CJK context.
- **Spanish `Ud.` / `Vd.` context splitting issue** ([#31](https://github.com/speedyk-005/yasbd-lib/pull/31)): Prevents incorrect sentence break when followed by proper nouns.
- **Reference abbreviation bracket edge case** ([#35](https://github.com/speedyk-005/yasbd-lib/pull/35)): Added `[` to lookahead set to prevent false boundary triggers.
- **Time-date pipeline cleanup (English-specific logic)** ([#40](https://github.com/speedyk-005/yasbd-lib/pull/40)): Ensures time/date handling is isolated to English rules without affecting other languages.

## [0.1.3] - 2026-06-01

### Fixed
- **Horizontal list finder over-match safety**: Restricts single-letter abbreviations (`p.`, `h.`, `s.`) from being incorrectly identified as alphabetic list markers by capping the range to `[a-eA-E]`.

## [0.1.2] - 2026-06-01

### Added
- **English golden benchmark suite (`EN_GOLDEN_DATA.py`)**: Introduced an 84-case golden validation set for English accuracy testing.
- **Golden benchmark execution runner (`run_golden.py`)**: Added an automated script to run accuracy comparisons across seven different libraries against the golden suite.
- **Expanded abbreviation coverage**: Added dozens of new terms across all core abbreviation categories (TITLE, REFERENCE, DATE, MID_SENTENCE, STREET, NAMES_WITH_EXCLAMATION).

### Changed
- **Trie-based pattern compilation** ([Commit 2c2f7df](https://github.com/speedyk-005/yasbd-lib/commit/2c2f7dfbeac91162c25df4ea5c2d17ea4150fdd7)): Replaced sorted `"|".join()` with `retrie.Trie` for optimized abbreviation regex generation.
- **Performance benchmarks rewrite**: Re-engineered cold/warm benchmarking tables, updated eight scenario tables with empirical runtimes, and appended accuracy metrics and conclusions.
- **Abbreviation logical redistribution**: Migrated shared tokens (e.g., `fr`, `ing`, `mme`) to the base configuration, allowing language-specific inheritance to handle localized overrides.
- **Pydantic version requirement relaxation**: Lowered the dependency constraint from `>=2.12.2` to `>=2.11.0` to maximize environment compatibility.

### Fixed
- **Module import error resolution**: Patched `boundary_detector.py` to stop swallowing unrelated import issues when a valid language class exists but lacks a sub-dependency.
- **PM/AM boundary false positives**: Excluded all-caps `P.M.` from being captured by the general acronym rules via targeted exclusions.

---

## [0.1.1] - 2026-05-30

### Fixed
- **Single-quote dialogue split bug** ([#23](https://github.com/speedyk-005/yasbd-lib/issues/34)): Fixed issues where the engine split text prematurely before a trailing dialogue tag (e.g., `'Is this great?' she said.`).
- **Ellipsis split suppression**: Prevented three-dot ellipsis (`...`) from acting as a terminal boundary, reserving splits strictly for four-dot boundaries.
- **Roman numeral initialism protection**: Stopped the pronoun `I` from triggering false sentence breaks in name strings like `Albert I. Jones`.
- **Numero reference split suppression**: Added `N°.` to the reference abbreviation lexicon to prevent false breaks.

### Changed
- **List finder regex backend migration**: Replaced standard regex search with `re2` to utilize lookbehinds, supporting non-Latin scripts via unicode class properties.

---

## [0.1.0] - 2026-05-29

Initial release.

### Added
- **Multilingual language engine**: Added core splitting support for 5 initial languages including English, French, Spanish, Haitian Creole, and Japanese.
- **Two-pass boundary engine**: Implements an optimized two-pass architecture featuring pre-processing rules and a main lookbehind abbreviation guard.
- **High-speed performance benchmark**: Tested speeds up to 16.5× faster than `pysbd` on 10.8K character benchmarking datasets.
- **Drop-in PySBD compatibility**: Included a drop-in `Segmenter` adapter that mirrors `pysbd`'s API interface, exposing `segment()`, `clean`, and `char_span` capabilities.
- **Flexible dual-mode API**: Exposes `detect()` for retrieving raw boundary offset slices and `segment()` for producing rich text string spans.
- **Comprehensive benchmarking harness**: Bundles comparative analysis scripts comparing seven libraries across seven distinct edge-case scenarios.
