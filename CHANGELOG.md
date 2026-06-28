# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.8.0] - Unreleased

### Added

- **py.typed marker** ([#116](https://github.com/speedyk-005/yasbd-lib/pull/116)): PEP 561 compliance marker for Mypy and Pyright static type checking.
- **Language pack system** ([#111](https://github.com/speedyk-005/yasbd-lib/pull/111)): `register_lang_packs()` with handshake validation and lang pack registry.
- **`LangPackError` exception class** ([#111](https://github.com/speedyk-005/yasbd-lib/pull/111)): raised when a language pack module fails validation or handshake.
- **Korean (ko) language support** ([#113](https://github.com/speedyk-005/yasbd-lib/pull/113)).
- **Dutch (nl) language support** ([#114](https://github.com/speedyk-005/yasbd-lib/pull/114)).
- **German military rank titles** ([#114](https://github.com/speedyk-005/yasbd-lib/pull/114)): Added to `TITLE_ABBRVS`.
- **Swedish (sv) language support** ([#121](https://github.com/speedyk-005/yasbd-lib/pull/121)).
- **Danish (da) language support** ([#121](https://github.com/speedyk-005/yasbd-lib/pull/121)).

### Changed

- **CJKV mixin** ([#115](https://github.com/speedyk-005/yasbd-lib/pull/115)): Shared full-width abbreviation pattern extracted from ``zh``, ``ja``, ``ko`` into ``base.py``.

### Fixed
- **German `DATE_ABBRVS`**: Removed "mai" — it's a full word, not an abbreviation.
- **ORDINAL regex (de, nl)** ([#114](https://github.com/speedyk-005/yasbd-lib/pull/114)): Changed `\d+` to `\d{1,3}` to avoid false sentence breaks after 3+ digit numbers.
- **Language tag normalization helper** ([#112](https://github.com/speedyk-005/yasbd-lib/pull/112)).
- **Thai discourse final particles**: Removed false positives `นะ` and `จ๋า` from `DISCOURSE_FINAL_PARTICLES`.
- **Burmese and Thai reporting words** ([#118](https://github.com/speedyk-005/yasbd-lib/pull/118)): Corrected attribute name from `REPORTING_VERBS` to `REPORTING_WORDS` — without this, the rules had no effect.

---

## [0.7.0] - 2026-06-22

### Added
- **Burmese (my) language support** ([#104](https://github.com/speedyk-005/yasbd-lib/pull/104)).
- **Hindi (hi) language support** ([#108](https://github.com/speedyk-005/yasbd-lib/pull/108)).

### Changed
- **CLI zero-copy file input** ([#107](https://github.com/speedyk-005/yasbd-lib/pull/107)): `--file` and stdin pipe now pass file handles directly to the detector instead of reading the entire file into memory first.
- **Refactored benchmark scripts** ([#105](https://github.com/speedyk-005/yasbd-lib/pull/105)): wrapped all benchmark scripts in `run_*` functions with `if __name__ == "__main__"` guards, migrated to `rich` console output, and cleaned up `bench_utils.py` (removed unused `langs` attributes, added docstrings, renamed `_console` for consistency).
- **Thai & Burmese ellipsis regex removal**: removed redundant `MID_SENTENCE_FINDER_LST` ellipsis pattern since `.` is not a sentence terminator in either language.
- **Input validation refactor** ([#106](https://github.com/speedyk-005/yasbd-lib/pull/106)): Replaced Pydantic's `validate_call` with beartype.

### Fixed
- **ParagraphStream auto-cleanup** ([#107](https://github.com/speedyk-005/yasbd-lib/pull/107)): added ``__del__`` and ``close()`` to ``ParagraphStream`` so opened file handles are closed on garbage collection.
- **List marker detection for non-Latin scripts** ([#103](https://github.com/speedyk-005/yasbd-lib/pull/103)): expanded `VERTICAL_LIST_START_FINDER` and `HORIZONTAL_LIST_FINDER` to accept Burmese, Devanagari, and other dot-like characters (။, ।, ·, •, etc.).
- **Thai & Burmese UTTERANCE_FINDER removal** ([#104](https://github.com/speedyk-005/yasbd-lib/pull/104)): removed `UTTERANCE_FINDER` and `STANDALONE_UTTERANCES` set from both `th.py` and `my.py` to prevent false sentence boundaries after discourse particles.

---

## [0.6.0] - 2026-06-15

### Added
- **spaCy v3+ pipeline component** ([#95](https://github.com/speedyk-005/yasbd-lib/pull/95)): Register yasbd as a native spaCy component, with lazy import guard and configurable via pipe.
- **Italian (it) language support** ([#99](https://github.com/speedyk-005/yasbd-lib/pull/99)).
- **Expanded base `TERMINATORS`** ([#96](https://github.com/speedyk-005/yasbd-lib/pull/96)): across major scripts (Armenian, Devanagari, Ethiopic, Mongolian, etc.) for better mixed-script support.
- **Book benchmarking script** ([#97](https://github.com/speedyk-005/yasbd-lib/pull/97)): `bench_books.py` benchmarks all SBD libraries on full-length books (Alice in Wonderland, Sherlock Holmes) with cold/warm timings and sentence counts.
- **Thai (th) language support** ([#100](https://github.com/speedyk-005/yasbd-lib/pull/100)): By far the hardest language to add — unicase, no word-boundary whitespace, punctuation used mainly in abbreviations, and discourse particles that required careful negative lookaheads to avoid double-splitting.
- **Greek (el) language support** ([#101](https://github.com/speedyk-005/yasbd-lib/pull/101)).
- **Expanded base `DOTTED_GEOPOL_ABBRVS`** ([#102](https://github.com/speedyk-005/yasbd-lib/pull/102)): major international organizations (N.A.T.O., U.N.E.S.C.O., W.H.O., etc.), regional bodies (A.U., O.A.S., A.S.E.A.N.), and additional sovereign state abbreviations.

### Changed
- **`QUOTATIVE_PARTICLES` renamed to `POST_QUOTATIVE_PARTICLES`** across all language rules to clarify they appear after quoted speech.

### Fixed
- **Conflict with quote/paren removal** ([#100](https://github.com/speedyk-005/yasbd-lib/pull/100)): reordered base pipeline so `_post_process_boundaries` runs before quote/paren spans are stripped.

---

## [0.5.0] - 2026-06-13

### Added
- **Automatic language detection** ([#86](https://github.com/speedyk-005/yasbd-lib/pull/86)): Pass `lang="auto"` to detect language via py3langid. Logs when confidence < 0.8.
- **`classify_language` utility** ([#86](https://github.com/speedyk-005/yasbd-lib/pull/86)): Wraps py3langid with softmax normalization and preference for supported languages.
- **Amharic (am) language support** ([#91](https://github.com/speedyk-005/yasbd-lib/pull/91)).

### Changed
- **Benchmarks expanded** ([#94](https://github.com/speedyk-005/yasbd-lib/pull/94)): EN golden data grew from 85 to 92 cases with academic citation patterns. Updated scores, refreshed cold/warm speed numbers, added per-language comparison links.
- **Internal refactors** ([#86](https://github.com/speedyk-005/yasbd-lib/pull/86)):
  - Cached up to 5 rule objects, evicting least recently used on overflow.
  - Moved `load_rule` because rule loading belongs to the rules package, not the detector.
  - Restructured `detect()` loop with first paragraph peeked before loop, uses `chain()` to rejoin — cleaner separation of EOF logic from content processing.
- **`NEWLINE_IN_MIDDLE_OF_WORD_FINDER` renamed to `NEWLINE_BETWEEN_WORD_CHARS`** and expanded pattern from `(?<=\b[a-zA-Z]{1,2})\n` to `(?<=\w)\n(?=\w)` to join mid-word newlines at any word-character boundary.

## [0.4.0] - 2026-06-10

### Added
- **`StreamCleaner` extra steps**: Custom cleaning functions run after the built-in pipeline. CLI via `--extra-step` / `-e` on `yasbd clean`, repeatable.
- **`CleanStepError`**: Raised when an extra step fails or returns non-string.
- **CLI short flags**: `-w` for `--preserve-whitespace`, `-r` for `--relative`.
- **Custom exception classes**: `YasbdError` (base), `UnsupportedLanguageError`, and `InvalidInputError` with ValueError/TypeError mixins.
- **Flat utils imports** ([#84](https://github.com/speedyk-005/yasbd-lib/pull/84)): Utils submodules now importable at package root via `__path__` extension — `from yasbd.cleaner import StreamCleaner` as an alternative to `from yasbd.utils.cleaner import StreamCleaner`.
- **Radicli-based CLI** ([#79](https://github.com/speedyk-005/yasbd-lib/pull/79)): `segment`, `detect`, `clean`, and `langs` subcommands with auto-stdin detection, JSONL output, and ~3.3x faster startup vs typer.

### Fixed
- **Emoji boundary detection** ([#77](https://github.com/speedyk-005/yasbd-lib/pull/77)): Emojis following terminal punctuation now stay with the preceding sentence. Besides, split after emoji + common sentence starter.
- **English `TITLE_ABBRVS`**: Excluded `min` to prevent false split suppression (minute/minimum should not suppress sentence boundaries).

### Changed
- **API doc generation** ([#83](https://github.com/speedyk-005/yasbd-lib/pull/83)): Replaced `python_docstring_markdown` with `pydoc-markdown`, fixing broken anchor links for re-exported symbols. Added `scripts/gen_api_docs.sh` for easy regeneration.
- **`log_info` helper**: Extracted to `yasbd.utils.logger` — gated logging without repeating `if verbose:`.
- **Unsupported language error messages** ([#78](https://github.com/speedyk-005/yasbd-lib/pull/78)): now list supported codes and suggest close matches (e.g. `eng` => `en`).
- **Variable renames for clarity**:
  - `MID_SENTENCE_ABBRVS` => `INLINE_ONLY_ABBRVS`
  - `HEADING_TOKENS` => `SECTION_MARKERS`
  - `GEOPOLITICAL_ABBRVS` => `DOTTED_GEOPOL_ABBRVS`
- **Spanish `COMMON_SENT_STARTERS` cleaned**: Removed 15 prepositions (En, Por, Para, De, etc.) and 15 verbs (Es, Son, Fue, Hay, etc.) that caused false sentence boundaries after `Ud.`/`Vd.` abbreviations.

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
- **Single-letter list marker false splits** ([#71](https://github.com/speedyk-005/yasbd-lib/pull/71)): Added context-aware heuristic to `_adjust_list_boundaries` so standalone "A." or "B." in prose are no longer split as list items.

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
